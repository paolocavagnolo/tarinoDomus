import asyncio
import serial
import requests
import configparser

config = ConfigParser.RawConfigParser()
config.read('../data.cfg')

hardware = 'mac'
hue_bridge_address = '192.168.1.2'

port = config.get(hardware, 'serial')
baudrate = config.getint(hardware, 'baudrate')
userId = config.get(hue,'id')

s = serial.Serial(port, baudrate)
url = 'http://' + hue_bridge_address + '/api/'

#get the map of the lights and create objects
r = requests.get(url)

#verify the objects
print(r.text)

#assigne every lights to every moteino_id_msg
###

print('Listening to the moteinos')
loop = asyncio.get_event_loop()
loop.add_reader(s, readSerial)

try:
    loop.run_forever()

except KeyboardInterrupt:
    pass

finally:
    loop.close()




def readSerial():
    text = ""
    msg = s.read().decode()
    while (msg != '\n'):
        text += msg
        msg = s.read().decode()
        moteinoId = msg.split(',')[0]
        buttonState = msg.split(',')[1]
    print(moteinoId)
    if (buttonState == '1'):
        print('pushed')
    if (buttonState == '2'):
        print('released')
    
        
    

