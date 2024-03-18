import logging

from azure.functions import EventHubEvent
from typing import List
import json
import os
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod


def run_camera(distance):
     if distance < 50:
            direct_method = CloudToDeviceMethod(method_name='camera_on', payload='{}')
            registry_manager_connection_string = os.environ['REGISTRY_MANAGER_CONNECTION_STRING']
            registry_manager = IoTHubRegistryManager(registry_manager_connection_string)
            camera_device_id='camera-sensor-allawy'
            registry_manager.invoke_device_method(camera_device_id, direct_method)

            logging.info('Direct method request sent! to {camera_device_id}')

def run_actuator(food_predictions):
     Reject_value = float(food_predictions["Reject"])
     Ripe_value = float(food_predictions["Ripe"])
     if Reject_value > Ripe_value:
            direct_method = CloudToDeviceMethod(method_name='red_led_on', payload='{}')
     else :
          direct_method = CloudToDeviceMethod(method_name='green_led_on', payload='{}')
     registry_manager_connection_string = os.environ['REGISTRY_MANAGER_CONNECTION_STRING']
     registry_manager = IoTHubRegistryManager(registry_manager_connection_string)
     actuator_device_id='acuator-allawy'
     registry_manager.invoke_device_method(actuator_device_id, direct_method)

     logging.info('Direct method request sent! to {actuator_device_id}')

             
def main(events: List[EventHubEvent]):
    for event in events:
        body = json.loads(event.get_body().decode('utf-8'))
        device_id = event.iothub_metadata['connection-device-id']

        logging.info(f'Received message: {body} from {device_id}')
        
        if device_id=='proximity-sensor-allawy':
            distance = body['distance']
            run_camera(distance)
        
        if device_id=='camera-sensor-allawy':
            food_predictions = body['food_predictions']
            run_actuator(food_predictions)
       
