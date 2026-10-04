import requests
import time
from pymodbus.client import ModbusTcpClient

# Configure your push service (Example: Pushover)

PUSHOVER_TOKEN = "your_app_token"
USER_KEY = "your_user_key"
PLC_IP = "127.0.0.1"

client = ModbusTcpClient(PLC_IP, port=502)
alarm_triggered = False

async def read_modbus():
    while True:
        print(f"Checking....")
        client.connect()
        # Read the coil monitoring your alarm condition
        #result = client.read_coils(1, count=1, device_id=1) 
        
        try:
            rr = await client.read_coils(1, count=1, device_id=1)
        except ModbusException as exc:
            _logger.error(f"ERROR: exception in pymodbus {exc}")
            raise exc
        if rr.isError():
            _logger.error("ERROR: pymodbus returned an error!")
            raise ModbusException(txt)

        if result.bits[0]:
            # Trigger the push notification
            '''
            requests.post("https://pushover.net", data={
                "token": PUSHOVER_TOKEN,
                "user": USER_KEY,
                "message": "Alert: OpenPLC detected a critical runtime event!"
            })
            '''
            print(f"True:")
            
            alarm_triggered = True # Prevent spamming
        elif not result.bits[0]:
            alarm_triggered = False
            
        time.sleep(1) # Poll every second


read_modbus()