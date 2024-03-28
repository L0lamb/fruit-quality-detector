import logging

from azure.functions import EventHubEvent
from typing import List
import json
import os
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod


def run_camera(distance):
     if distance < 50:
          #Create a direct method to turn on the camera
            direct_method = CloudToDeviceMethod(method_name='camera_on', payload='{}')
          #Get the connection string for the IoTHub Registry Manager from environment variables
            registry_manager_connection_string = os.environ['REGISTRY_MANAGER_CONNECTION_STRING']
          #Initialize IoTHub Registry Manager
            registry_manager = IoTHubRegistryManager(registry_manager_connection_string)
          #Define the camera device ID
            camera_device_id='camera-sensor-allawy'
          #Invoke the direct method on the camera device
            registry_manager.invoke_device_method(camera_device_id, direct_method)
          #Log a message
            logging.info('Direct method request sent! to {camera_device_id}')

def run_actuator(food_predictions):
     #Extract values for rejection and ripeness predictions
     Reject_value = float(food_predictions["Reject"])
     Ripe_value = float(food_predictions["Ripe"])
     #Create a direct method to turn on the red or green LED
     if Reject_value > Ripe_value:
            direct_method = CloudToDeviceMethod(method_name='red_led_on', payload='{}')
     else :
          direct_method = CloudToDeviceMethod(method_name='green_led_on', payload='{}')
     #Get the connection string for the IoTHub Registry Manager from environment variables
     registry_manager_connection_string = os.environ['REGISTRY_MANAGER_CONNECTION_STRING']
     #Initialize IoTHub Registry Manager
     registry_manager = IoTHubRegistryManager(registry_manager_connection_string)
     #Set the actuator device ID
     actuator_device_id='acuator-allawy'
     #Invoke the direct method on the actuator device
     registry_manager.invoke_device_method(actuator_device_id, direct_method)
     #Log message that the Dirrect message has been sent to the register acuator
     logging.info('Direct method request sent! to {actuator_device_id}')

             
def main(events: List[EventHubEvent]):
    for event in events:
          #Decode the event body as JSON
        body = json.loads(event.get_body().decode('utf-8'))
         #Extract the device ID from event metadata
        device_id = event.iothub_metadata['connection-device-id']
          #Log message showing the received message and its source device ID
        logging.info(f'Received message: {body} from {device_id}')
        
        if device_id=='proximity-sensor-allawy':
            distance = body['distance']
            run_camera(distance)
     #Check distance to activate camera based on proximity
         
        if device_id=='camera-sensor-allawy':
            food_predictions = body['food_predictions']
            run_actuator(food_predictions)
       #Extract the data and handle the actuator control based on 'food_prediction'
