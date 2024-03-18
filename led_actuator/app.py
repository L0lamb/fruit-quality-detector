import time
from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.grove_led import GroveLed

from azure.iot.device import IoTHubDeviceClient, MethodResponse


CounterFitConnection.init('127.0.0.1', 5000)

red_led = GroveLed(1)
green_led = GroveLed(2)

connection_string = ''

device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)

print('Connecting')
device_client.connect()
print('Connected')

def handle_method_request(request):
    
    if request.name == "red_led_on":
        print("Direct method received - ", request.name)
        red_led.on()
        green_led.off()
    if request.name == "green_led_on":
        print("Direct method received - ", request.name)
        red_led.off()
        green_led.on()

    method_response = MethodResponse.create_from_method_request(request, 200)
    device_client.send_method_response(method_response)

device_client.on_method_request_received = handle_method_request

while True:
    time.sleep(5)