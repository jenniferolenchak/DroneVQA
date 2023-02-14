# Visual Inspection and Deep Learning

## Table of Contents
- [About](#about)
- [Members and Roles](#members-and-roles)
- [Visual Question Answering](#visual-question-answering)
- [Multimodal Transformers](#multimodal-transformers)
- [Models](#models)

## About
UCF Senior Design Project, Sponsored by Lockheed Martin \
Deep learning for visual inspection performed by simulated drones

## Members and Roles
- Samuel Hearn
- Jennifer Olenchak, _Project Manager_
- Marco Peric, _Dataset Creation & Training Lead_
- Robin Perlman, _Model Research & Deployment Lead_
- Ayden Rebhan
- Brandon Spangler

## Visual Question Answering

VQA is a computer vision task where a model is given a text question about an image, and the model must infer an answer.

## Multimodal Transformers

![transformer architecture](https://d2l.ai/_images/transformer.svg)
*Source: Attention is All You Need (2017)*

* Transformer models utilize "self-attention" to weigh significant aspects of an input
* Transformer models use "positional encoding", and an entire input sequence can be run in parallel (great for speed and scalability)
* Encoder / Decoder Architecture 
    * The models we work with only contain encoders
    * Decoders can be used for generative text
* A multimodal transformer combines two or more different types of input data
    * For us, an image and text are the two inputs

## Models

The two models selected were ViLT and LXMERT. The goal is to compare these models (both base and fine-tuned versions) to see which would work best for the purposes of real time VQA and explainable AI.

* ### VILT (Vision and Language Transformer)

![ViLT model architecture](https://production-media.paperswithcode.com/methods/e99bcb9b-eecf-4a7e-acb6-8e03c70e8261.png)
*Source: ViLT: Vision-and-Language Transformer Without Convolution or Region Supervision (2021)*

* ViLT is a simplified architecture which encodeds the text and image input together. This makes is very fast and it still have comparable results to state of the art models.
* ViLT was not designed with visual grounding in mind and thus visual grounding results can be poor.

* ### LXMERT (Learn Cross-Modality Encoder Representations from Transformers)

![LXMERT model architecture](https://miro.medium.com/max/1031/1*6-2JubfCcKzaKs0jIgg52w.png)
*Source: LXMERT: Learning Cross-Modality Encoder Representations from Transformers (2019)*

* LXMERT relies on a Faster RCNN backbone to obtain 36 object detections which are passed as input into the model. This backbone model requires more time for computation and slows down the results, but LXMERT can be useful for visual grounding purposes.




