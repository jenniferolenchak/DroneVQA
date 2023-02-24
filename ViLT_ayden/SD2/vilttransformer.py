import json
from transformers import ViltProcessor, ViltForQuestionAnswering, ViltConfig
from PIL import Image
import re
from typing import Optional
from os import listdir
from os.path import isfile, join
from tqdm.notebook import tqdm
import torch
from torch.utils.data import DataLoader

#open questions
f = open("C:/Users/ayden/Documents/GitHub/VisualInspectionDeepLearning/ViLT_ayden/SD2/v2_OpenEnded_mscoco_train2014_questions.json")
data_questions = json.load(f)
questions = data_questions['questions']

#begin assigning questions ids
filename_re = re.compile(r".*(\d{12})\.((jpg)|(png))")
def id_from_filename(filename: str) -> Optional[int]:
    match = filename_re.fullmatch(filename)
    if match is None:
        return None
    return int(match.group(1))

#root for folder of images
root = "C:/Users/ayden/Documents/GitHub/VisualInspectionDeepLearning/ViLT_ayden/SD2/vqatraining/train2014/train2014"

#begin assigning images to questions
file_names = [f for f in listdir(root) if isfile(join(root, f))]

filename_to_id = {root + "/" + file: id_from_filename(file) for file in file_names}
id_to_filename = {v:k for k,v in filename_to_id.items()}

path = id_to_filename[questions[0]['image_id']]
image = Image.open(path)

#open annotations/answers
f = open("C:/Users/ayden/Documents/GitHub/VisualInspectionDeepLearning/ViLT_ayden/SD2/v2_mscoco_train2014_annotations.json")

#load annotations
data_annotations = json.load(f)
annotations = data_annotations['annotations']

#config
config = ViltConfig.from_pretrained("dandelin/vilt-b32-finetuned-vqa")

def get_score(count: int) -> float:
    return min(1.0, count / 3)

for annotation in tqdm(annotations):
    answers = annotation['answers']
    answer_count = {}
    for answer in answers:
        answer_ = answer["answer"]
        answer_count[answer_] = answer_count.get(answer_, 0) + 1
    labels = []
    scores = []
    for answer in answer_count:
        if answer not in list(config.label2id.keys()):
            continue
        labels.append(config.label2id[answer])
        score = get_score(answer_count[answer])
        scores.append(score)
    annotation['labels'] = labels
    annotation['scores'] = scores

#verify labels
labels = annotations[0]['labels']
print([config.id2label[label] for label in labels])    

#print scores
scores = annotations[0]['scores']
print(scores)

#begin torch dataset
class VQADataset(torch.utils.data.Dataset):
    def __init__(self, questions, annotations, processor):
        self.questions = questions
        self.annotations = annotations
        self.processor = processor

    def __len__(self):
        return len(self.annotations)

    def __getitem__(self, idx):
        # get image + text
        annotation = self.annotations[idx]
        questions = self.questions[idx]
        image = Image.open(id_to_filename[annotation['image_id']])
        text = questions['question']
        
        encoding = self.processor(image, text, padding="max_length", truncation=True, return_tensors="pt")
        # remove batch dimension
        for k,v in encoding.items():
          encoding[k] = v.squeeze()
        # add labels
        labels = annotation['labels']
        scores = annotation['scores']
        targets = torch.zeros(len(config.id2label))
        for label, score in zip(labels, scores):
              targets[label] = score
        encoding["labels"] = targets

        return encoding

#select pretrained model    
processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-mlm")

#select dataset
dataset = VQADataset(questions=questions[:100],
                     annotations=annotations[:100],
                     processor=processor)

labels = torch.nonzero(dataset[0]['labels']).squeeze().tolist()


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-mlm",
                                                 num_labels=len(config.id2label),
                                                 id2label=config.id2label,
                                                 label2id=config.label2id)
model.to(device)

def collate_fn(batch):
  input_ids = [item['input_ids'] for item in batch]
  pixel_values = [item['pixel_values'] for item in batch]
  attention_mask = [item['attention_mask'] for item in batch]
  token_type_ids = [item['token_type_ids'] for item in batch]
  labels = [item['labels'] for item in batch]
  
  # create padded pixel values and corresponding pixel mask
  encoding = processor.feature_extractor.pad_and_create_pixel_mask(pixel_values, return_tensors="pt")
  
  # create new batch
  batch = {}
  batch['input_ids'] = torch.stack(input_ids)
  batch['attention_mask'] = torch.stack(attention_mask)
  batch['token_type_ids'] = torch.stack(token_type_ids)
  batch['pixel_values'] = encoding['pixel_values']
  batch['pixel_mask'] = encoding['pixel_mask']
  batch['labels'] = torch.stack(labels)
  
  return batch

train_dataloader = DataLoader(dataset, collate_fn=collate_fn, batch_size=4, shuffle=True)

batch = next(iter(train_dataloader))

optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)

model.train()
for epoch in range(50):  # loop over the dataset multiple times
   print(f"Epoch: {epoch}")
   for batch in tqdm(train_dataloader):
        # get the inputs; 
        batch = {k:v.to(device) for k,v in batch.items()}

        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        outputs = model(**batch)
        loss = outputs.loss
        print("Loss:", loss.item())
        loss.backward()
        optimizer.step()

torch.save(model, "C:/Users/ayden/Documents/GitHub/VisualInspectionDeepLearning/ViLT_ayden/SD2/finetunedvilt.pt")