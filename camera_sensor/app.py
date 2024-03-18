from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5000)
import json
import time
import io
import requests
from counterfit_shims_picamera import PiCamera
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse


camera = PiCamera()
camera.resolution = (640, 480)
camera.rotation = 0

connection_string = ''

device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)

print('Connecting')
device_client.connect()
print('Connected')

def handle_method_request(request):
    
    if request.name == "camera_on":
        print("Direct method received - ", request.name)
        image = io.BytesIO()
        camera.capture(image, 'jpeg')
        image.seek(0)

        with open('image.jpg', 'wb') as image_file:
            image_file.write(image.read())

        prediction_url = ' http://127.0.0.1:80/image'
        headers = {
            'Content-Type' : 'application/octet-stream'
        }
        image.seek(0)
        response = requests.post(prediction_url, headers=headers, data=image)
        results = response.json()
        data={
            results["predictions"][0]["tagName"]:f'{results["predictions"][0]["probability"]*1:.2f}',
            results["predictions"][1]["tagName"]:f'{results["predictions"][1]["probability"]*1:.2f}'
            }
        # for prediction in results['predictions']:
        #     data={prediction["tagName"]:f'{prediction["probability"] * 100.00:.2f}%'}
            # print(f'{prediction["tagName"]}:\t{prediction["probability"] * 100:.2f}%')
        print(data)
        message = Message(json.dumps({ 'food_predictions': data }))
        device_client.send_message(message)
    method_response = MethodResponse.create_from_method_request(request, 200)
    device_client.send_method_response(method_response)


device_client.on_method_request_received = handle_method_request

while True:
     time.sleep(5)