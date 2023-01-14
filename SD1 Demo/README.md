
# AirSim Demo

## Goal
This AirSim Demo is mean to be a simple demonstration of the desired capabilities for our project. It shows that we can obtain a live video feed from the AirSim Environment and perform Visual Question Answering using a Transformer model

## Running the demo

1. Open AirSim and select quadcopter
2. Run the main.py file
3. Initialize the AirSim Client
4. Ask a Question and Perform a Prediction

## VQA Demos

The VQA Demos showcase multimodal transformer options for our real time VQA goal. These serve as a basis for demonstration of the capabilities of each model. We will use this information when deciding on how to proceed with the project

You can run each of the VQA notebooks to see how each model is running. Take note of the accuracy and computation time of each model.

## Notes
Place the settings.json file into the directory containing the Microsoft AirSim executable file. This file is used specifically to alter settings about the 
AirSim, such as the resolution of images used for our model.

See https://microsoft.github.io/AirSim/image_apis/ for information about the settings and camera parameters