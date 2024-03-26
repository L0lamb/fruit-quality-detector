from counterfit_connection import CounterFitConnection #imports the CounterFitConnection class from the counterfit_connection module
CounterFitConnection.init('127.0.0.1', 5000) #connect to the counter fit app on port 5000
import json
import time
import io
import requests
from counterfit_shims_picamera import PiCamera #import Picamera for the counterfit library
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse
# The device connection string to authenticate the device with your IoT hub.

camera = PiCamera()
#create PiCamera object
camera.resolution = (640, 480)
#set resolution
camera.rotation = 0
#set image rotation

connection_string = ''
#indicate where to store the Connection strings

device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)
#create a device client object that can communicate with IoT Hub, and connect it

print('Connecting') #?
device_client.connect() #Oh? it connected?
print('Connected') #We show em it connected

def handle_method_request(request): #define a method that will be called when a dirrect method is called bt the IOT hub
    
    if request.name == "camera_on":
        print("Direct method received - ", request.name)
        image = io.BytesIO() 
        camera.capture(image, 'jpeg') #set and define the object and class
        image.seek(0) # Seeks to the given frame in this sequence file

        with open('image.jpg', 'wb') as image_file: #opens a file called image.jpg for writing, then reads all the data from the BytesIO object and writes that to the file.
            image_file.write(image.read())

        prediction_url = ' http://127.0.0.1:80/image' #The pic Url
        headers = {
            'Content-Type' : 'application/octet-stream' #define the content type as octet-stream
        }
        image.seek(0)
        response = requests.post(prediction_url, headers=headers, data=image)
        #Sending a POST request to the prediction URL with the image data and headers
        results = response.json()
        #Parsing the JSON response received from the prediction service
        data={
            results["predictions"][0]["tagName"]:f'{results["predictions"][0]["probability"]*1:.2f}', #Acessing the top prediction and its probability
            results["predictions"][1]["tagName"]:f'{results["predictions"][1]["probability"]*1:.2f}' #Acess the second top prediction and its probability
            }
        # for prediction in results['predictions']:
        #     data={prediction["tagName"]:f'{prediction["probability"] * 100.00:.2f}%'}
            # print(f'{prediction["tagName"]}:\t{prediction["probability"] * 100:.2f}%')
        print(data)
        message = Message(json.dumps({ 'food_predictions': data }))
        #Creating a message containing the food predictions data in JSON format
        device_client.send_message(message)
        #Sending the message containing the predictions data to the device client
    method_response = MethodResponse.create_from_method_request(request, 200)
    #Method request work? Me show method response
    device_client.send_method_response(method_response)
    #send the method_response back to the client


device_client.on_method_request_received = handle_method_request

while True:
     time.sleep(5) #repeat 5 times
