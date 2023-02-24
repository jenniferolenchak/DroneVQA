import os
from transformers import ViltForQuestionAnswering, ViltProcessor 
import torch

from dataclasses import dataclass, field

# Imports related to LXMERT
from PIL import Image
from transformers import LxmertForQuestionAnswering, LxmertTokenizer
from frcnn.utils import Config, get_data
from frcnn.modeling_frcnn import GeneralizedRCNN
from frcnn.processing_image import Preprocess
from frcnn.visualizing_image import SingleImageViz


# class to store relevant prediction information
@dataclass
class PredictionResults:
    # Initial Question Information
    question: str
    image: any

    # Prediction
    prediction: str

    # Extra Visualization Data. These are optional
    top_predictions: list[tuple[str, float]] = field(default_factory=list[tuple[str, float]])
    visualizations: list = field(default_factory=list)

# ViLT Model
def predictVilt(model, processor, question, image):
    encoding = processor(image, question, return_tensors="pt")

    outputs = model(**encoding)
    logits = outputs.logits
    idx = torch.sigmoid(logits).argmax(-1).item()

    # Get Top Answers
    sm = torch.nn.Softmax(dim=0)
    probabilities = sm(logits[0])
    top_answer_ids = list(probabilities.argsort()[-5:])
    top_predictions = []
    for id in top_answer_ids:
        answer : str = model.config.id2label[id.item()]
        prob : float = probabilities[id.item()]
        top_predictions.append((answer, prob))

    results = PredictionResults(question=question, image=image, 
                                prediction=model.config.id2label[idx],
                                top_predictions=top_predictions)

    return results

def setupViltTransformer():
    processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
    model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")

    return model, processor

def setupTunedViltTransformer():
    processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
    model = ViltForQuestionAnswering.from_pretrained("finetunedvilt.pt")
    model.to(device)

    return model, processor

# LXMERT Model
IMAGE_LOCATION = r"./FRCNN_Image.jpg"

def setupLxmertTransformer():

    # Define the model
    lxmert_tokenizer = LxmertTokenizer.from_pretrained("unc-nlp/lxmert-base-uncased")
    lxmert_vqa = LxmertForQuestionAnswering.from_pretrained("unc-nlp/lxmert-vqa-uncased")

    # Setup Faster RCNN Model for visual embeddings (backbone)
    frcnn_cfg = Config.from_pretrained("unc-nlp/frcnn-vg-finetuned")
    frcnn = GeneralizedRCNN.from_pretrained("unc-nlp/frcnn-vg-finetuned", config=frcnn_cfg)
    image_preprocess = Preprocess(frcnn_cfg)

    return lxmert_tokenizer, lxmert_vqa, frcnn_cfg, frcnn, image_preprocess

def runFRCNN(image, image_preprocess, frcnn, frcnn_cfg):
    # Save a temporary copy of the image for the model
    #print(f"image type {type(image)}")
    im = Image.fromarray(image)
    im.save(IMAGE_LOCATION)

    # run frcnn
    images, sizes, scales_yx = image_preprocess(IMAGE_LOCATION)
    output_dict = frcnn(
        images,
        sizes,
        scales_yx=scales_yx,
        padding="max_detections",
        max_detections=frcnn_cfg.max_detections,
        return_tensors="pt",
    )

    visualization = visualizeBoxes(output_dict)

    # Delete image copy
    os.remove(IMAGE_LOCATION)
    print(output_dict.keys())

    return output_dict, visualization

def visualizeBoxes(output_dict):
    # Image Visualization
    OBJ_URL = "https://raw.githubusercontent.com/airsplay/py-bottom-up-attention/master/demo/data/genome/1600-400-20/objects_vocab.txt"
    ATTR_URL = "https://raw.githubusercontent.com/airsplay/py-bottom-up-attention/master/demo/data/genome/1600-400-20/attributes_vocab.txt"

    objids = get_data(OBJ_URL)
    attrids = get_data(ATTR_URL)

    frcnn_visualizer = SingleImageViz(IMAGE_LOCATION, id2obj=objids, id2attr=attrids)

    # add boxes and labels to the image
    frcnn_visualizer.draw_boxes(
        output_dict.get("boxes"),
        output_dict.pop("obj_ids"),
        output_dict.pop("obj_probs"),
        output_dict.pop("attr_ids"),
        output_dict.pop("attr_probs"),
    )

    # Return Visualized Image
    return frcnn_visualizer._get_buffer()

def predictLxmert(lxmert_tokenizer, lxmert_vqa, frcnn_cfg, frcnn, image_preprocess, question, image):
    output_dict, visualization = runFRCNN(image, image_preprocess, frcnn, frcnn_cfg) 

    # Very important that the boxes are normalized
    normalized_boxes = output_dict.get("normalized_boxes")
    features = output_dict.get("roi_features")

    VQA_URL = "https://raw.githubusercontent.com/airsplay/lxmert/master/data/vqa/trainval_label2ans.json"
    vqa_answers = get_data(VQA_URL)

    inputs = lxmert_tokenizer(
        [question],
        padding="max_length",
        max_length=20,
        truncation=True,
        return_token_type_ids=True,
        return_attention_mask=True,
        add_special_tokens=True,
        return_tensors="pt",
    )

    # run lxmert
    output_vqa = lxmert_vqa(
        input_ids=inputs.input_ids,
        attention_mask=inputs.attention_mask,
        visual_feats=features,
        visual_pos=normalized_boxes,
        token_type_ids=inputs.token_type_ids,
        output_attentions=False,
    )
    # get prediction
    pred_vqa = output_vqa["question_answering_score"].argmax(-1)
    print("Question:", question)
    print("prediction from LXMERT VQA:", vqa_answers[pred_vqa])

    # TODO: Obtain top 5 predictions and probabilities

    results = PredictionResults(question=question[0], image=image, prediction=vqa_answers[pred_vqa], 
                                visualizations=[visualization])

    return results