<p align="center">
    This University of Central Florida senior design project is sponsored by the Lockheed Martin Corporation.
    <br/><br/>
    <img src="/Application/Images/Logos/DroneVQALogo.png" />
</p>

# Table of Contents
- [About](#about)
- [Setting Up & Getting Started](#setting-up-and-getting-started)
- [Application User Guide](#application-user-guide)
    - [Loading Screen](#loading-screen)
    - [Launch Screen](#launch-screen)
    - [VQA Interaction Screen](#vqa-interaction-screen)
- [Members and Roles](#members-and-roles)
- [Visual Question Answering](#visual-question-answering)
- [Multimodal Transformers](#multimodal-transformers)
- [Models](#models)
- [Model Input and Output Specifications](#model-input-and-output-specifications)
- [Visualization Methods](#visualization-methods)
- [LXMERT Model Training and Fine-tuning Process](#lxmert-model-training-and-fine-tuning-process)
  - [Setup for Model Training and Procedure](#setup-for-model-training-and-procedure)
  - [Training/Fine-tuning Notes](#trainingfine-tuning-notes)

<br/><br/>

# About
**DroneVQA: Deploying Transformer-Based Visual Question Answering (VQA) Artificial Intelligence Models on Simulated Quadrotor Drones to Perform Visual Inspection**

&nbsp;&nbsp;&nbsp;&nbsp;
This simulation-based proof-of-concept deploys two transformer-based open-source visual question answering (VQA) artificial intelligence models on the camera feed of simulated drones to perform visual inspection of simulated environments. Drones are ideal candidates for performing visual inspection, as they are easily maneuverable, remotely relocatable, able to self-navigate, and allow for dynamic perspectives. Developed by Hugging Face, the ViLT (Vision-and-Language Transformer Without Convolution or Region Supervision) and LXMERT (Learning Cross-Modality Encoder Representations from Transformers) models can provide an 'answer' when passed a natural language string accompanied by an image. The real-world applications of this technology suite are limitless, enabling autonomous complex surveillance, environmental monitoring, situational-analysis, self-inspection, and maintenance support.

&nbsp;&nbsp;&nbsp;&nbsp;
This project takes a research-based approach to compare the performance of open-source models among one another, as well as ease of fine-tuning for drone usage, by comparing key factors including answer accuracy, topic understanding, processing speed, and model training improvement.  Using the cross-platform, desktop-based DroneVQA software tool developed in Python with QT Creator and PySide 6, users can fly a drone around virtual environments and ask questions about what the drone’s camera sees. To demystify the functionality of VQA models, explainable AI (XAI) result visualizations are generated to display the provided prompt and image from the perspective of the AI model, highlighting key aspects which informed the model’s conclusion along with the top answer weights. Users may also elect to simulate environmental weather effects such as rain, snow, dust, and fog, as well as camera defects including lens blur, pixel corruption, and disconnection, which are vital to evaluate self-inspection abilities and real-world model robustness.

<br/><br/>

# Setting Up and Getting Started
1. Clone the repository using one of the following options:    
    - __[Option 1]__ Using SSH:
        ```
        git clone git@github.com:jenniferolenchak/DroneVQA.git
        ```
    - __[Option 2]__ Using HTTPS:
        ```
        git clone https://github.com/jenniferolenchak/DroneVQA.git
        ```
    
2. Download a copy of each fine-tuned model file, ```FineTunedLXMERT.pth``` and ```FineTunedVILT.pt```, from this [shared OneDrive folder](https://knightsucfedu39751-my.sharepoint.com/:f:/g/personal/jenniferolenchak_knights_ucf_edu/EqXwJqszeqFIj6-7diRTAF0BriSv1i0XW1dK_nvBrsvL6Q?e=MKbdYZ). These two files must be placed within the existing folder [/Application/Fine-Tuned Models/](https://github.com/jenniferolenchak/DroneVQA/tree/main/Application/Fine-Tuned%20Models) such that the filepaths ```/Application/Fine-Tuned Models/FineTunedLXMERT.pth``` and ```/Application/Fine-Tuned Models/FineTunedVILT.pt``` can be referenced.
    
3. Install python and pip. This application was developed using python v3.10 and pip v22.3, but newer versions may also be functional.

4. Download the necessary python packages to enable the application to run on your system. This can be accomplished using any of the following methods:

    - __[Option 1]__ Batch install all required packages using ```pip``` by entering the following command in the top-level directory of the cloned repository:
        ```
        pip install -r requirements.txt
        ```
    
    - __[Option 2]__ Install the required packages individually using ```pip``` for each version/package pair listed in [requirements.txt](https://github.com/jenniferolenchak/DroneVQA/blob/main/requirements.txt). For example, the first pip command should be entered as:
        ```
        pip install airsim==1.8.1
        ```

    - __[Option 3]__ Set up a venv python virtual environment by executing the command in the top-level directory of the cloned repository:
        ```
        python setup_environment.py
        ```

    - __[Option 4]__ If you wish to run the faster RCNN backbone on your GPU, rather than on your CPU, for major LXMERT performance improvements:

        1. Manually create a new virtual environment and activate this new environment.

        2. Review https://pytorch.org/ for an installation with cuda. The installation command should look like:    
        ```pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu117```

        3. Then install the rest of the dependencies:   
        ```pip install -r requirements.txt```

5. Download an Unreal Engine environment that has the Microsoft AirSim plug-in enabled. Choose one of the following options:
    - __[Option 1]__ Download the file(s) of an officially released Unreal Engine V4 environment containing the Microsoft AirSim plug-in from [https://github.com/microsoft/AirSim/releases](https://github.com/microsoft/AirSim/releases). Once the environment ZIP file has been downloaded, extract the file(s) using 7-zip and run the ```run.bat``` file. Further details about downloading and extracting the large environment files are available via the above link.

    - __[Option 2]__ Download the Unreal Engine V5 city map developed for use by this project, available [here](https://knightsucfedu39751-my.sharepoint.com/:u:/g/personal/georgec_knights_ucf_edu/EX_7FaD9tp5KrDsan_br704Bzd5CeatU0i3EkygkDceTcQ?e=owa42D).

    - __[Option 3]__ You may also choose to use your own Unreal Engine environment, but the Microsoft AirSim plug-in must be enabled and properly configured using the Unreal Editor in order to work with this application.

6. Launch the DroneVQA application by navigating to the ```/DroneVQA/Application``` directory and executing the following command:
    ```
    python application.py
    ```
    If the above steps were successfully completed, a [Loading Screen](#loading-screen) should immediately appear and be replaced by a [Launch Screen](#launch-screen) when loading has concluded.

7. Launch the Unreal Engine environment executable when prompted by the application, once the [Launch Screen](#launch-screen) has been reached. From here, follow the directions listed within the application.

8. Enjoy! We recommend that the the [Application User Guide](#application-user-guide) be reviewed for any necessary clarification about supported features.

<br/><br/>
# Application User Guide

## Loading Screen
The loading screen is the first screen seen upon starting the application. If it is your first time starting the application the loading screen will take longer. However, this is only on first-time start-up, and starting the application again will result in a faster loading time.

<p align='center'>
    <img src='Application%20Screenshots/Loading_Screen.png' height='75%' width='75%'/>
</p>

<br/><br/>
## Launch Screen
This is the first interactive screen that you will see. Here you will find the instructions to setup and start the Unreal Environment with the Microsoft AirSim plugin. After following those instructions click on 'Initialize Client.' 

<p align='center'>
    <img src='Application%20Screenshots/Launch_Screen.png' height='55%' width='55%'/>
</p>

If everything is working properly then the VQA screen with appear, if not an error message will popup.

<p align='center'>
    <img src='Application%20Screenshots/Launch_Error.png' height='55%' width='55%'/>
</p>

<br/><br/>
## VQA Interaction Screen
This is the main screen of the application. Here you can see the live drone video feed, control the drone and environment weather, change specific camera effects, and ask your questions. 

<p align='center'>
    <img src='Application%20Screenshots/VQA_Screen.png' height='75%' width='75%'/>
</p>

<br/><br/>
### Drone Feed
The drone camera feed section has three main features. Firstly, there is the freeze frame and snapshot buttons. The freeze frame only freezes the video feed and not the simulation in the background. The 'Take a Snapshot' button saves the current image to the 'Exports and Snapshot' in the locally created directory. The camera effect radio buttons are singular toggles that change the effects of the current image. These changes are reflected on the image passed into the ViLT and LXMERT models.

<p align='center'>
    <img src='Application%20Screenshots/Drone_feed.png' height='75%' width='75%'/>
</p>

<br/><br/>
### Flight Controls, AirSim Utility Buttons, and Weather Controls
Below the drone camera feed is the flight controls, AirSim utility buttons, and the weather controls. The flight controls have a velocity slider which changes how fast the drone moves. There are also directional buttons allowing for full control of the drone. The AirSim utility buttons allow for control of the drone simulation in the event of unexpected behavior or the desire to reset to starting conditions. The weather and environment sliders provide options to control the simulation environment. It is important to note that these sliders will only affect the environment if the current Unreal Environment supports and includes the necessary weather assets. 

<p align='center'>
    <img src='Application%20Screenshots/Drone_controls.png' height='75%' width='75%'/>
</p>

<br/><br/>
### Model Interaction and Visualizations
On the right side of the VQA Screen is the model interaction. Here you can ask your question, select your model, and export results. The results to your question will appear in the 'Results' box. If exporting, the results are saved in .docx and .JSON format in the 'Exports and Snapshots' local directory. After asking your question model visualizations and results will appear. Depending on the selected model different visualizations are generated. Below are examples from both the ViLT and LXMERT models. 

<p align='center'>
    <img src='Application%20Screenshots/ViLT_example.png' height='75%' width='75%'/>
    <br/>
    <em>ViLT Question and Result Example</em>
</p>

<p align='center'>
    <img src='Application%20Screenshots/LXMERT_example.png' height='75%' width='75%'/>
    <br/>
    <em>LXMERT Question and Result Example</em>
</p>


These questions can be anything, but tailoring to the current environment will help produce better results. Additionally, asking simpler questions will tend to produce more accurate, concise results. 

<br/><br/>
# Members and Roles
| Name  | GitHub Username | Role |
| ------------- | ------------- | ------------- |
| Samuel Hearn | @SADPuppett |
| Jennifer Olenchak | @jenniferolenchak | _Project Manager, Application Lead_|
| Marco Peric | @marcoperic | _Dataset Creation & Training Lead_ |
| Robin Perlman | @Perl-R |  _Model Research & Deployment Lead_ |
| Ayden Rebhan | @ayden-rebhan |
| Brandon Spangler  | @brandonspangler2 |

<br/><br/>
# Visual Question Answering
VQA is a computer vision task where a model is given a text question about an image, and the model must infer an answer.

<br/><br/>
# Multimodal Transformers
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
# Models
The two models selected were ViLT and LXMERT. The goal is to compare these models (both base and fine-tuned versions) to see which would work best for the purposes of real time VQA and explainable AI.

<br/><br/>
## VILT (Vision and Language Transformer) <!-- omit from toc --> 

![ViLT model architecture](https://production-media.paperswithcode.com/methods/e99bcb9b-eecf-4a7e-acb6-8e03c70e8261.png)   
*Source: ViLT: Vision-and-Language Transformer Without Convolution or Region Supervision (2021)*

* ViLT is a simplified architecture which encodeds the text and image input together. This makes is very fast and it still have comparable results to state of the art models.
* ViLT was not designed with visual grounding in mind and thus visual grounding results can be poor.

<br/><br/>
## LXMERT (Learn Cross-Modality Encoder Representations from Transformers) <!-- omit from toc --> 

![LXMERT model architecture](https://miro.medium.com/max/1031/1*6-2JubfCcKzaKs0jIgg52w.png)   
*Source: LXMERT: Learning Cross-Modality Encoder Representations from Transformers (2019)*

* LXMERT relies on a Faster RCNN backbone to obtain 36 object detections which are passed as input into the model. This backbone model requires more time for computation and slows down the results, but LXMERT can be useful for visual grounding purposes.

<br/><br/>
# Model Input and Output Specifications

## VILT 

* Input
    * VILT takes a 640x384 image as input. 
    * The ViltProcessor will automatically resize the shorter edge of an image to 384 and limit the longer edge to under 640 while preserving the aspect ratio.
    * VILT utilizes the BERT Tokenizer to tokenize input text.

* Output
    * For VQA Tasks, VILT will select the most appropriate response from 3,129 answer classes.

<br/><br/>
## LXMERT

* Input
    * LXMERT's FasterRCNN backbone resizes images to a size of no larger than 1333x800. It then produces up to 36 detections (each with a feature map of size 2048) for the LXMERT model.
    * LXMERT utilizes the LXMERT Tokenizer to tokenize input text.

* Output
    * For VQA Tasks, LXMERT will select the most appropriate response from 3,129 answer classes.


<br/><br/>
# Visualization Methods

## VILT Visualization Methods <!-- omit from toc --> 

* The original paper for VILT proposes generating a heatmap on the image for each input text token. Each tile on the image represents a patch, and its opacity represents how pertinent it was to the text token.

* A technique called Inexact Promixal Point Method of Optimal Transports (IPOT) is used to generate these alignment scores between the textual and visual subsets of the model encoding.

* As a result, there is a visualization for each attention token. There is also a combined visualization which shows the overall attention by combining all of the individual heatmaps.

<br/><br/>
## LXMERT Visualization Methods <!-- omit from toc --> 

* The four visualizations for the LXMERT model are:
1. Faster RCNN Object Detections
2. Attention Rollout
3. Gradcam
4. Chefer Explainability

* The faster RCNN object detections are shown a visualization on screen. The faster RCNN model produces up to 36 object detections for the LXMERT model. 

* Attention Rollout is designed for visualizing attention based on the visual self-attention layers. The visualizations tend to give an wholistic view of all detections which are important to the model

* Gradcam (Gradient-weighted Class Activation Mapping) utilizes the classification of the model and the gradients leading to it to determine which parts of the input image were most impactful in generating the prediction. Note: Gradcam does not look at the Cross-Modality Encoder of LXMERT and focuses only on the Object-Relationship Encoder.

* Chefer Explainability is described in the paper "Generic Attention-model Explainability for Interpreting Bi-Modal and Encoder-Decoder Transformers" (2021) and its corresponding repository: https://github.com/hila-chefer/Transformer-MM-Explainability. It is a method of developing XAI visualizations with multimodal transformers. The method uses model self- and co- attention layers to "produce relevancy maps for each of the interactions between input modalities in the network." 

![LXMERT Visualization](https://raw.githubusercontent.com/hila-chefer/Transformer-MM-Explainability/main/LXMERT.PNG)
*Chefer Explainability      
Source: Generic Attention-model Explainability for Interpreting Bi-Modal and Encoder-Decoder Transformers (2021)*

<br/><br/>
# LXMERT Model Training and Fine-tuning Process

## Setup for Model Training and Procedure
The LXMERT training and fine-tuning procedure uses the [official LXMERT repository](https://github.com/airsplay/lxmert), and more specifically, the pre-training and VQA fine-tuning sections of the repository. After downloading a pre-trained model, it is possible to fine-tune it by default with the MSCOCO dataset, but we are using our custom Unreal Engine v5 Airsim Dataset, which contains questions and labels for the model to learn from. 

<br/><br/>
## Training/Fine-tuning Notes
Fine-tuning is taking place on an NVIDIA RTX 3070 Ti.
Some specifics include:
* 9 llayers
* 5 xlayers
* 5 rlayers
* Batch size of 32
* Learning rate of 5e-5

Furthermore, there were some issues with memory fragmentation, as the 3070 Ti only has 8GB of VRAM available. As such, the following fixes were explored:
* Reduced batch size
* Offloaded model to CPU
* Different optimizers were tried
* Exclusive CPU training
* PYTORCH_CUDA_ALLOC_CONF parameter set to 324MB (working solution!)
