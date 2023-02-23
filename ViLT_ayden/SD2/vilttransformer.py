import json
from transformers import ViltProcessor, ViltForQuestionAnswering
from PIL import Image

#dataset
dataset = open("C:/Users/ayden/Documents/GitHub/VisualInspectionDeepLearning/ViLT_ayden/SD2/training.json")
data_questions = json.load(dataset)
#still working on getting this working


#basic vilt VQA model for testing
image = Image.open("C:/Users/ayden/Documents/GitHub/VisualInspectionDeepLearning/ViLT_ayden/SD2/dataset/0ba6GMWh07_jpg.rf.a77c73c953dd171e52111e80290c9997.jpg")
text = "whats the weather like?"

processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")

encoding = processor(image, text, return_tensors="pt")

outputs = model(**encoding)
logits = outputs.logits
idx = logits.argmax(-1).item()
print("Predicted answer:", model.config.id2label[idx])