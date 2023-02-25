import os
from transformers import ViltForQuestionAnswering, ViltProcessor 
import torch
import numpy as np

from dataclasses import dataclass, field

# Imports related to LXMERT
from PIL import Image
from transformers import LxmertForQuestionAnswering, LxmertTokenizer
from frcnn.utils import Config, get_data
from frcnn.modeling_frcnn import GeneralizedRCNN
from frcnn.processing_image import Preprocess
from frcnn.visualizing_image import SingleImageViz
from ModelVisualizations.vilt_visualization import get_visualization_for_token, combine_images, rgba2rgb

device = "cuda:0" if torch.cuda.is_available() else "cpu"

# class to store relevant prediction information
@dataclass
class PredictionResults:
    # Initial Question Information
    question: str
    image: any

    # Model Used
    model_used: str

    # Prediction
    prediction: str

    # Extra Visualization Data. These are optional
    top_predictions: list[tuple[str, float]] = field(default_factory=list[tuple[str, float]])
    visualizations: list = field(default_factory=list[np.ndarray]) # This is a list of RGB images (CV2 images)

    # Token information:
    encoded_tokens: list = field(default_factory=list)
    decoded_tokens: list = field(default_factory=list)

# ViLT Model
def predictVilt(model, processor, question, image):
    encoding = processor(image, question, return_tensors="pt").to(device)

    outputs = model(**encoding)
    logits = outputs.logits
    idx = torch.sigmoid(logits).argmax(-1).item()

    # Get Top Answers
    top_predictions = getTopPredictions(logits[0], model.config.id2label)

    # Obtain the tokens used as input
    encoded_tokens = encoding['input_ids'].tolist()[0]
    decoded_tokens = [processor.tokenizer.convert_ids_to_tokens(token) for token in encoded_tokens]

    # Visualizations
    _, visuals = get_visualization_for_token(model, encoding, image)
    visualizations = []
    visualizations.append(combine_images(visuals))
    visualizations.extend(visuals)
    visualizations = [rgba2rgb(np.array(visual)) for visual in visualizations]

    results = PredictionResults(question=question, image=image,
                                model_used='ViLT', 
                                prediction=model.config.id2label[idx],
                                top_predictions=top_predictions,
                                encoded_tokens=encoded_tokens, decoded_tokens=decoded_tokens,
                                visualizations=visualizations
                                )

    return results

def setupViltTransformer():
    processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
    model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
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

def setupLxmertTransformer_finetuned():

    # Define the model
    lxmert_tokenizer = LxmertTokenizer.from_pretrained("unc-nlp/lxmert-base-uncased")
    lxmert_vqa_finetuned = LxmertForQuestionAnswering.from_pretrained(pretrained_model_name_or_path='lxmert_best_model.pth', config='config.json')

    # Setup Faster RCNN Model for visual embeddings (backbone)
    frcnn_cfg = Config.from_pretrained("unc-nlp/frcnn-vg-finetuned")
    frcnn = GeneralizedRCNN.from_pretrained("unc-nlp/frcnn-vg-finetuned", config=frcnn_cfg)
    image_preprocess = Preprocess(frcnn_cfg)

    # add lxmert_vqa_finetuned to this list. 
    return lxmert_tokenizer, lxmert_vqa_finetuned, frcnn_cfg, frcnn, image_preprocess

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

    # Get top predicted answer index
    pred_vqa = output_vqa["question_answering_score"].argmax(-1)

    # Get Top Answers
    top_predictions = getTopPredictions(output_vqa["question_answering_score"][0], vqa_answers)

    # Obtain the tokens used as input
    encoded_tokens = inputs['input_ids'].tolist()[0]
    decoded_tokens = [lxmert_tokenizer.convert_ids_to_tokens(token) for token in encoded_tokens]

    results = PredictionResults(question=question, image=image, 
                                model_used='LXMERT', 
                                prediction=vqa_answers[pred_vqa], 
                                top_predictions=top_predictions, visualizations=[visualization],
                                encoded_tokens=encoded_tokens, decoded_tokens=decoded_tokens)

    return results

def getTopPredictions(vqa_raw_scores, vocab_dictionary):
    '''
    vqa_raw_scores is a Tensor containing the final classification scores of the model

    vocab_dictionary is a dictionary mapping the model output indicies to the corresponding words

    Returns a list of tuples with a word and corresponding score
    '''
    sm = torch.nn.Softmax(dim=0)
    probabilities = sm(vqa_raw_scores)
    top_answer_ids = probabilities.argsort()[-5:]
    top_predictions = []
    for id in top_answer_ids:
        id = int(id) # Type conversion to ensure we are working with ints and not tensors
        answer : str = vocab_dictionary[id]
        prob : float = probabilities[id]
        top_predictions.append((answer, prob))
    
    return top_predictions[::-1] # Reverse so we show results in descending order
