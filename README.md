<p align="center">
    This University of Central Florida senior design project is sponsored by the Lockheed Martin Corporation.
    <br/><br/>
    <img src="/Application/Images/Logos/DroneVQALogo.png" />
</p>

## Table of Contents
- [About](#about)
- [Getting Started](#getting-started)
- [Members and Roles](#members-and-roles)
- [Visual Question Answering](#visual-question-answering)
- [Multimodal Transformers](#multimodal-transformers)
- [Models](#models)

<br/><br/>
## About
**Utilizing Artificial Intelligence to Deploy Visual Question Answering on Simulated Quadrotor Drones for Visual Inspection**

&nbsp;&nbsp;&nbsp;&nbsp;
This simulation-based proof-of-concept deploys open-source visual question answering (VQA) artificial intelligence models on the camera feed of simulated drones to perform visual inspection of simulated environments. Drones are ideal candidates for performing visual inspection, as they are easily maneuverable, remotely relocatable, able to self-navigate, and allow for dynamic perspectives. The real-world applications of this technology are limitless, enabling autonomous complex surveillance, environmental monitoring, situational-analysis, self-inspection, and maintenance support.

&nbsp;&nbsp;&nbsp;&nbsp;
This project takes a research-based approach to compare the performance of open-source models among one another, as well as before and after they are fine-tuned for drone usage, by comparing key factors including answer accuracy, topic understanding, processing speed, and model training improvement. Using the DroneVQA desktop-based software tool, users can fly a drone around virtual environments and ask questions about what the drone’s camera sees. To demystify the functionality of VQA models, result visualizations displaying the exact image pixels or object-detection results that informed the model’s conclusion are provided along with the top answers. Users may also elect to simulate environmental weather effects such as rain, snow, dust, and fog, as well as camera defects including lens blur, pixel corruption, and disconnection, vital to evaluate self-inspection abilities and real-world model robustness.

<br/><br/>
## Getting Started
1. Clone the repository using one of the following options:
    a) Using SSH:
    ```
    git clone git@github.com:jenniferolenchak/DroneVQA.git
    ```
    b) Using HTTPS:
    ```
    git clone https://github.com/jenniferolenchak/DroneVQA.git
    ```
    
2. Install python and pip. This application was developed using python v3.10 and pip v22.3, but newer versions may also be functional.

3. In the top-level directory of the cloned repository, set up the venv python virtual environment by executing the following command:
    ```
    python setup_environment.py
    ```
    *If you wish to install the required packages using a different method, the ```requirements.txt``` file has been provided within this repository.

4. Download the ZIP file of an Unreal Engine environment containing the Microsoft AirSim plug-in. Officially released environments are available for download on GitHub [here](https://github.com/microsoft/AirSim/releases).

5. Once the environment ZIP file has been downloaded, extract the file(s) and run the ```run.bat``` file.

6. With the virtual environment activated, launch the DroneVQA application, navigate to the ```/DroneVQA/Application``` directory and execute the following command:
    ```
    python application.py
    ```

7. Launch the environment executable when prompted by the application.

<br/><br/>
## Members and Roles
| Name  | GitHub Username | Role |
| ------------- | ------------- | ------------- |
| Samuel Hearn | @SADPuppett |
| Jennifer Olenchak | @jenniferolenchak | _Project Manager_ |
| Marco Peric | @marcoperic | _Dataset Creation & Training Lead_ |
| Robin Perlman | @Perl-R |  _Model Research & Deployment Lead_ |
| Ayden Rebhan | @ayden-rebhan |
| Brandon Spangler  | @brandonspangler2 |

<br/><br/>
## Visual Question Answering
VQA is a computer vision task where a model is given a text question about an image, and the model must infer an answer.

<br/><br/>
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

<br/><br/>
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
