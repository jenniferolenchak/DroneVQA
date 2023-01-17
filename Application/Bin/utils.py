import cv2
import numpy as np
from transformers import ViltForQuestionAnswering, ViltProcessor 
import torch
import threading
from multiprocessing import Process

from dataclasses import dataclass, field

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

