# LXMERT visualization generator. Based on work from: https://github.com/hila-chefer/Transformer-MM-Explainability

import torch
import cv2
import copy

# Visualization Creator Function
# Note: For best results, open the saved visualization
def create_image_vis(img, image_scores, rcnn_dict: dict, output_path: str) -> str:
    bbox_scores = image_scores

    mask = torch.zeros(img.shape[0], img.shape[1])
    print(mask.shape)

    for index in range(len(bbox_scores)):
        
        [x, y, w, h] = rcnn_dict.get("boxes")[0][index]
        curr_score_tensor = mask[int(y):int(h), int(x):int(w)]
        new_score_tensor = torch.ones_like(curr_score_tensor)*bbox_scores[index].item()
        mask[int(y):int(h), int(x):int(w)] = torch.max(new_score_tensor,mask[int(y):int(h), int(x):int(w)])

    mask = (mask - mask.min()) / (mask.max() - mask.min())
    mask = mask.unsqueeze_(-1)
    mask = mask.expand(img.shape)
    img_multiplier = mask.numpy()
    img = img * img_multiplier
    img *= (255.0/img.max())

    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

    # Note: For some reason, the images don't display nicely unless they are written as files and then opened again
    cv2.imwrite(output_path, img)
    return output_path

# Extra Rules and Visualization Helper Functions

def compute_rollout_attention(all_layer_matrices, start_layer=0):
    # adding residual consideration
    num_tokens = all_layer_matrices[0].shape[1]
    eye = torch.eye(num_tokens).to(all_layer_matrices[0].device)
    all_layer_matrices = [all_layer_matrices[i] + eye for i in range(len(all_layer_matrices))]
    matrices_aug = [all_layer_matrices[i] / all_layer_matrices[i].sum(dim=-1, keepdim=True)
                          for i in range(len(all_layer_matrices))]
    joint_attention = matrices_aug[start_layer]
    for i in range(start_layer+1, len(matrices_aug)):
        joint_attention = matrices_aug[i].matmul(joint_attention)
    return joint_attention

# rule 5 from paper
def avg_heads(cam, grad):
    cam = cam.reshape(-1, cam.shape[-2], cam.shape[-1])
    grad = grad.reshape(-1, grad.shape[-2], grad.shape[-1])
    cam = grad * cam
    cam = cam.clamp(min=0).mean(dim=0)
    return cam

# rules 6 + 7 from paper
def apply_self_attention_rules(R_ss, R_sq, cam_ss):
    R_sq_addition = torch.matmul(cam_ss, R_sq)
    R_ss_addition = torch.matmul(cam_ss, R_ss)
    return R_ss_addition, R_sq_addition

# rules 10 + 11 from paper
def apply_mm_attention_rules(R_ss, R_qq, R_qs, cam_sq, apply_normalization=True, apply_self_in_rule_10=True):
    apply_normalization = False # Note: We don't apply normalization as it can assertion errors for some cases
    R_ss_normalized = R_ss
    R_qq_normalized = R_qq
    if apply_normalization:
        R_ss_normalized = handle_residual(R_ss)
        R_qq_normalized = handle_residual(R_qq)
    R_sq_addition = torch.matmul(R_ss_normalized.t(), torch.matmul(cam_sq, R_qq_normalized))
    if not apply_self_in_rule_10:
        R_sq_addition = cam_sq
    R_ss_addition = torch.matmul(cam_sq, R_qs)
    return R_sq_addition, R_ss_addition

# normalization- eq. 8+9
def handle_residual(orig_self_attention):
    self_attention = orig_self_attention.clone()
    diag_idx = range(self_attention.shape[-1])
    # computing R hat
    self_attention -= torch.eye(self_attention.shape[-1]).to(self_attention.device)
    
    assert self_attention[diag_idx, diag_idx].min() >= 0
    
    # normalizing R hat
    self_attention = self_attention / self_attention.sum(dim=-1, keepdim=True)
    self_attention += torch.eye(self_attention.shape[-1]).to(self_attention.device)
    return self_attention

# Supports Bi-Modal Transformer Explainability, Gradcam, and Attention Rollout
class LxmertVisualizationGenerator: 
    def __init__(self, model, rcnn_dict: dict, inputs, outputs, save_visualization=False):
        self.model = model
        self.rcnn_dict = rcnn_dict
        self.inputs = inputs
        self.outputs = outputs
        self.save_visualization = save_visualization

    def _gradcam(self, cam, grad):
        cam = cam.reshape(-1, cam.shape[-2], cam.shape[-1]) # Becomes (12, 36, 20)
        grad = grad.reshape(-1, grad.shape[-2], grad.shape[-1]) 
        grad = grad.mean(dim=[1, 2], keepdim=True)
        cam = (cam * grad).mean(0).clamp(min=0)
        
        return cam

    def generate_attn_gradcam(self, index=None, method_name="gradcam"):
        output = self.outputs.question_answering_score
        model = self.model

        # initialize relevancy matrices
        text_tokens = len(self.inputs.input_ids.flatten()) # By default question length is 20
        image_bboxes = self.rcnn_dict.get("roi_features").shape[1] # Max of 36 Boxes for LXMERT

        # text self attention matrix
        self.R_t_t = torch.eye(text_tokens, text_tokens).to(model.device)
        # image self attention matrix
        self.R_i_i = torch.eye(image_bboxes, image_bboxes).to(model.device)
        # impact of images on text
        self.R_t_i = torch.zeros(text_tokens, image_bboxes).to(model.device)
        # impact of text on images
        self.R_i_t = torch.zeros(image_bboxes, text_tokens).to(model.device)


        if index == None:
            index = np.argmax(output.cpu().data.numpy(), axis=-1)

        one_hot = np.zeros((1, output.size()[-1]), dtype=np.float32)
        one_hot[0, index] = 1
        one_hot = torch.from_numpy(one_hot).requires_grad_(True)
        one_hot = torch.sum(one_hot * output)

        model.zero_grad()
        one_hot.backward(retain_graph=True)

        # last cross attention + self- attention layer
        blk = model.lxmert.encoder.x_layers[-1]
        # cross attn cam will be the one used for the R_t_i matrix        
        grad_t_i = blk.visual_attention.att.get_attn_gradients()[-1].detach()
        cam_t_i = blk.visual_attention.att.get_attn()[-1].detach()
        cam_t_i = self._gradcam(cam_t_i, grad_t_i)
        # self.R_t_i = torch.matmul(self.R_t_t.t(), torch.matmul(cam_t_i, self.R_i_i))
        self.R_t_i = cam_t_i

        # language self attention
        grad = blk.lang_self_att.self.get_attn_gradients()[-1].detach()
        cam = blk.lang_self_att.self.get_attn()[-1].detach()
        self.R_t_t = self._gradcam(cam, grad)

        # disregard the [CLS] token itself
        self.R_t_t[0, 0] = 0
        return self.R_t_t, self.R_t_i
    
    def generate_rollout(self, method_name="rollout"):
        output = self.outputs.question_answering_score
        model = self.model

        # initialize relevancy matrices
        text_tokens = len(self.inputs.input_ids.flatten()) # By default question length is 20
        image_bboxes = self.rcnn_dict.get("roi_features").shape[1] # Max of 36 Boxes for LXMERT

        # text self attention matrix
        self.R_t_t = torch.eye(text_tokens, text_tokens).to(model.device)
        # image self attention matrix
        self.R_i_i = torch.eye(image_bboxes, image_bboxes).to(model.device)
        # impact of images on text
        self.R_t_i = torch.zeros(text_tokens, image_bboxes).to(model.device)
        # impact of text on images
        self.R_i_t = torch.zeros(image_bboxes, text_tokens).to(model.device)

        cams_text = []
        cams_image = []
        # language self attention
        blocks = model.lxmert.encoder.layer
        for blk in blocks:
            cam = blk.attention.self.get_attn()[-1].detach()
            cam = cam.reshape(-1, cam.shape[-2], cam.shape[-1]).mean(dim=0)
            cams_text.append(cam)


        # image self attention
        blocks = model.lxmert.encoder.r_layers
        for blk in blocks:
            cam = blk.attention.self.get_attn()[-1].detach()
            cam = cam.reshape(-1, cam.shape[-2], cam.shape[-1]).mean(dim=0)
            cams_image.append(cam)

        # cross attn layers
        blocks = model.lxmert.encoder.x_layers
        for i, blk in enumerate(blocks):
            # in the last cross attention module, only the text cross modal
            # attention has an impact on the CLS token, since it's the first
            # token in the language tokens
            if i == len(blocks) - 1:
                break

            # language self attention
            cam = blk.lang_self_att.self.get_attn()[-1].detach()
            cam = cam.reshape(-1, cam.shape[-2], cam.shape[-1]).mean(dim=0)
            cams_text.append(cam)

            # image self attention
            cam = blk.visn_self_att.self.get_attn()[-1].detach()
            cam = cam.reshape(-1, cam.shape[-2], cam.shape[-1]).mean(dim=0)
            cams_image.append(cam)


        # take care of last cross attention layer- only text
        blk = model.lxmert.encoder.x_layers[-1]
        # cross attn cam will be the one used for the R_t_i matrix
        cam_t_i = blk.visual_attention.att.get_attn()[-1].detach()
        cam_t_i = cam_t_i.reshape(-1, cam_t_i.shape[-2], cam_t_i.shape[-1]).mean(dim=0)
        self.R_t_t = compute_rollout_attention(copy.deepcopy(cams_text))
        self.R_i_i = compute_rollout_attention(cams_image)
        self.R_t_i = torch.matmul(self.R_t_t.t(), torch.matmul(cam_t_i, self.R_i_i))
        
        #self.R_t_i = torch.matmul(self.R_t_t.t(), torch.matmul(cam_t_i, self.R_i_i))
        # language self attention
        cam = blk.lang_self_att.self.get_attn()[-1].detach()
        cam = cam.reshape(-1, cam.shape[-2], cam.shape[-1]).mean(dim=0)
        cams_text.append(cam)

        self.R_t_t = compute_rollout_attention(cams_text)

        # disregard the [CLS] token itself
        self.R_t_t[0,0] = 0
        return self.R_t_t, self.R_t_i
    
    def _handle_self_attention_lang(self, blocks):
        for blk in blocks:
            grad = blk.attention.self.get_attn_gradients()[-1].detach()
            if self.use_lrp:
                cam = blk.attention.self.get_attn_cam()[-1].detach()
            else:
                cam = blk.attention.self.get_attn()[-1].detach()
            cam = avg_heads(cam, grad)
            R_t_t_add, R_t_i_add = apply_self_attention_rules(self.R_t_t, self.R_t_i, cam)
            self.R_t_t += R_t_t_add
            self.R_t_i += R_t_i_add

    def _handle_self_attention_image(self, blocks):
        for blk in blocks:
            grad = blk.attention.self.get_attn_gradients()[-1].detach()
            if self.use_lrp:
                cam = blk.attention.self.get_attn_cam()[-1].detach()
            else:
                cam = blk.attention.self.get_attn()[-1].detach()
            cam = avg_heads(cam, grad)
            R_i_i_add, R_i_t_add = apply_self_attention_rules(self.R_i_i, self.R_i_t, cam)
            self.R_i_i += R_i_i_add
            self.R_i_t += R_i_t_add

    def _handle_co_attn_self_lang(self, block):
        grad = block.lang_self_att.self.get_attn_gradients().detach()
        if self.use_lrp:
            cam = block.lang_self_att.self.get_attn_cam()[-1].detach()
        else:
            cam = block.lang_self_att.self.get_attn()[-1].detach()
        cam = avg_heads(cam, grad)
        R_t_t_add, R_t_i_add = apply_self_attention_rules(self.R_t_t, self.R_t_i, cam)
        self.R_t_t += R_t_t_add
        self.R_t_i += R_t_i_add

    def _handle_co_attn_self_image(self, block):
        grad = block.visn_self_att.self.get_attn_gradients()[-1].detach()
        if self.use_lrp:
            cam = block.visn_self_att.self.get_attn_cam()[-1].detach()
        else:
            cam = block.visn_self_att.self.get_attn()[-1].detach()
        cam = avg_heads(cam, grad)
        R_i_i_add, R_i_t_add = apply_self_attention_rules(self.R_i_i, self.R_i_t, cam)
        self.R_i_i += R_i_i_add
        self.R_i_t += R_i_t_add

    def _handle_co_attn_lang(self, block):
        if self.use_lrp:
            cam_t_i = block.visual_attention.att.get_attn_cam()[-1].detach()
        else:
            cam_t_i = block.visual_attention.att.get_attn()[-1].detach()
        grad_t_i = block.visual_attention.att.get_attn_gradients()[-1].detach()
        cam_t_i = avg_heads(cam_t_i, grad_t_i)
        R_t_i_addition, R_t_t_addition = apply_mm_attention_rules(self.R_t_t, self.R_i_i, self.R_i_t, cam_t_i,
                                                                  apply_normalization=self.normalize_self_attention,
                                                                  apply_self_in_rule_10=self.apply_self_in_rule_10)
        return R_t_i_addition, R_t_t_addition

    def _handle_co_attn_image(self, block):
        if self.use_lrp:
            cam_i_t = block.visual_attention_copy.att.get_attn_cam()[-1].detach()
        else:
            cam_i_t = block.visual_attention_copy.att.get_attn()[-1].detach()
        grad_i_t = block.visual_attention_copy.att.get_attn_gradients().detach()
        cam_i_t = avg_heads(cam_i_t, grad_i_t)
        R_i_t_addition, R_i_i_addition = apply_mm_attention_rules(self.R_i_i, self.R_t_t, self.R_t_i, cam_i_t,
                                                                  apply_normalization=self.normalize_self_attention,
                                                                  apply_self_in_rule_10=self.apply_self_in_rule_10)
        return R_i_t_addition, R_i_i_addition

    def generate_ours(self, index=None, use_lrp=True, normalize_self_attention=True, apply_self_in_rule_10=True, method_name="ours"):
        self.use_lrp = use_lrp
        self.use_lrp = False

        self.normalize_self_attention = normalize_self_attention
        self.apply_self_in_rule_10 = apply_self_in_rule_10
        kwargs = {"alpha": 1}
        output = self.outputs.question_answering_score
        model = self.model

        # initialize relevancy matrices
        text_tokens = len(self.inputs.input_ids.flatten()) # By default question length is 20
        image_bboxes = self.rcnn_dict.get("roi_features").shape[1] # Max of 36 Boxes for LXMERT

        # text self attention matrix
        self.R_t_t = torch.eye(text_tokens, text_tokens).to(model.device)
        # image self attention matrix
        self.R_i_i = torch.eye(image_bboxes, image_bboxes).to(model.device)
        # impact of images on text
        self.R_t_i = torch.zeros(text_tokens, image_bboxes).to(model.device)
        # impact of text on images
        self.R_i_t = torch.zeros(image_bboxes, text_tokens).to(model.device)

        if index is None:
            index = np.argmax(output.cpu().data.numpy(), axis=-1)

        one_hot = np.zeros((1, output.size()[-1]), dtype=np.float32)
        one_hot[0, index] = 1
        one_hot_vector = one_hot
        one_hot = torch.from_numpy(one_hot).requires_grad_(True)
        # one_hot = torch.sum(one_hot.cuda() * output)
        one_hot = torch.sum(one_hot * output) # Currently don't support cuda. Make sure to fix cuda dependencies


        model.zero_grad()
        one_hot.backward(retain_graph=True)
        if self.use_lrp:
            model.relprop(torch.tensor(one_hot_vector).to(output.device), **kwargs)

        # language self attention
        blocks = model.lxmert.encoder.layer
        self._handle_self_attention_lang(blocks)

        # image self attention
        blocks = model.lxmert.encoder.r_layers
        self._handle_self_attention_image(blocks)

        # cross attn layers
        blocks = model.lxmert.encoder.x_layers
        for i, blk in enumerate(blocks):
            # in the last cross attention module, only the text cross modal
            # attention has an impact on the CLS token, since it's the first
            # token in the language tokens
            if i == len(blocks) - 1:
                break
            # cross attn- first for language then for image
            R_t_i_addition, R_t_t_addition = self._handle_co_attn_lang(blk)
            R_i_t_addition, R_i_i_addition = self._handle_co_attn_image(blk)

            self.R_t_i += R_t_i_addition
            self.R_t_t += R_t_t_addition
            self.R_i_t += R_i_t_addition
            self.R_i_i += R_i_i_addition

            # language self attention
            self._handle_co_attn_self_lang(blk)

            # image self attention
            self._handle_co_attn_self_image(blk)


        # take care of last cross attention layer- only text
        blk = model.lxmert.encoder.x_layers[-1]
        # cross attn- first for language then for image
        R_t_i_addition, R_t_t_addition = self._handle_co_attn_lang(blk)
        self.R_t_i += R_t_i_addition
        self.R_t_t += R_t_t_addition

        # language self attention
        self._handle_co_attn_self_lang(blk)

        # disregard the [CLS] token itself
        self.R_t_t[0,0] = 0
        return self.R_t_t, self.R_t_i