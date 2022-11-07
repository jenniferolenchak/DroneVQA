import PySimpleGUI as sg
import airsim
import cv2
import numpy as np
from transformers import ViltForQuestionAnswering, ViltProcessor 
import torch

def setupTransformer():
    processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
    model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")

    return model, processor


def main():
    sg.theme("LightGreen")

    # Define the window layout
    layout = [
        [sg.Text("AirSim VQA Demo", size=(60, 1), justification="center")],
        [sg.Image(key='-IMAGE-')],
        [sg.Text("Live Video Feed")],
        [sg.Button("Init AirSim Client")],
        [sg.InputText(key="-QUESTION-")],
        [sg.Button("Predict")],
        [sg.Text("Answer:"), sg.Text("", key="-ANSWER-")],
        [sg.Button("Stop")],
        [sg.Button("Exit")],
    ]

    # Create the window
    window = sg.Window("AirSim VQA Demo", layout, location=(800, 400))

    record = False
    model, processor = None, None

    while True:
        event, values = window.read(timeout=20)
        if event == "Exit" or event == sg.WIN_CLOSED:
            print("Exiting")
            break

        elif event == "Init AirSim Client":
            client = airsim.MultirotorClient()
            client.confirmConnection()
            client.enableApiControl(True)
            client.armDisarm(True)

            # Async methods returns Future. Call join() to wait for task to complete.
            client.takeoffAsync().join()
            client.moveToPositionAsync(-10, 10, -10, 5).join()

            print("Finished Moving")

            CAMERA_NAME = '0'
            IMAGE_TYPE = airsim.ImageType.Scene
            DECODE_EXTENSION = '.png'
        
            record = True

        elif event == "Predict":
            if model == None or processor == None:
                model, processor = setupTransformer()

            # Get the most recent image from our live feed and obtain question from user
            image = decoded_frame
            question = values["-QUESTION-"]
            print(question)

            # forward pass
            encoding = processor(image, question, return_tensors="pt")

            outputs = model(**encoding)
            logits = outputs.logits
            idx = torch.sigmoid(logits).argmax(-1).item()

            # Display Output
            print("Predicted answer:", model.config.id2label[idx])
            window["-ANSWER-"].update(model.config.id2label[idx])
                        
        elif event == "Stop":
            record = False
            img = np.full((720, 1280), 255)
            # this is faster, shorter and needs less includes
            imgbytes = cv2.imencode('.png', img)[1].tobytes()
            window['-IMAGE-'].update(data=imgbytes)

        if record:
            # Get Feed From AirSim
            response_image = client.simGetImage(CAMERA_NAME, IMAGE_TYPE)
            np_response_image = np.asarray(bytearray(response_image), dtype="uint8")
            decoded_frame = cv2.imdecode(np_response_image, cv2.IMREAD_COLOR)
            ret, encoded_png = cv2.imencode(DECODE_EXTENSION, decoded_frame)
            frame = encoded_png.tobytes()

            cv2.imwrite('AirSimImage.png', decoded_frame)

            # Note: PySimpleGui's Image only works with .png and .gif formats. We need to convert to png instead of .jpg
            window['-IMAGE-'].update(data=frame)


    window.close()

main()