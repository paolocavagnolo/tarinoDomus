import asyncio
import serial
import requests
import configparser

s = serial.Serial('/dev/pts/13', 9600)
url = 'https://192.168.1.2/api/'



def readSerial():
    text = ""
    msg = s.read().decode()
    while (msg != '\n'):
        text += msg
        msg = s.read().decode()
    print(text)
    loop.call_soon(s.write, "ok\n".encode())

loop = asyncio.get_event_loop()
loop.add_reader(s, readSerial)

try:
    loop.run_forever()

except KeyboardInterrupt:
    pass

finally:
    loop.close()