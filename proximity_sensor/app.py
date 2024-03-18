from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5000)

import time
import json
from counterfit_shims_rpi_vl53l0x.vl53l0x import VL53L0X

from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse

connection_string = ''

device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)

print('Connecting')
device_client.connect()
print('Connected')



distance_sensor = VL53L0X(address= 0x00)
distance_sensor.begin()

while True:
    if distance_sensor.wait_ready():
        distance = distance_sensor.get_distance()
        print(f'Distance = {distance} mm')
        message = Message(json.dumps({ 'distance': distance }))
        device_client.send_message(message)
    time.sleep(10)