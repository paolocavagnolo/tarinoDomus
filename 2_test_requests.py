import asyncio
import requests
import sys
import json
import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 115200)

hue_key = 'xsNe1CZ71oiR-Awe-OBkT6E4ZcbflRyDNnx4WDsB'
url = 'http://192.168.1.2/api/' + hue_key + '/'

#global
light_state = [False,False]
start_time = 0
counter = 0
brightness = 254
a_pushed = False

def read_and_do():
	msg = []
	inCh = ser.readline().decode()

	if (len(inCh) > 10):

		msg = inCh.split(',')

		if (len(msg) > 2) and (len(msg) < 9):
			lights(msg)

async def conta( start_time ):
	global counter, brightness, a_pushed
	await asyncio.sleep(2)
	dataj = {"on":True}
	if (a_pushed):
		req = requests.put(url + 'lights/1/state',json = dataj)
	step = 50
	while (a_pushed):
		if (brightness > 249):
			brightness = 250
			step = -25
		elif (brightness <= 0):
			brightness = 0
			step = 25

		brightness = brightness + step

		dataj = {"bri":brightness}
		req = requests.put(url + 'lights/1/state',json = dataj)
		await asyncio.sleep(0.1)


def lights( input_list ):
	global counter, a_pushed

	if int(input_list[5]) == 61:
		if int(input_list[6]) == 31:
			print("A pushed")
			a_pushed = True
			asyncio.ensure_future(conta(time.time()))
			print("ok")


		if int(input_list[6]) == 32:
			a_pushed = False
			print("A released")
			light_state[0] = not light_state[0]
			dataj = {"on":light_state[0]}
			req = requests.put(url + 'lights/1/state',json = dataj)
			counter = counter + 1
			print(req.text)

	if int(input_list[5]) == 62:
		if int(input_list[6]) == 32:
			print("B released")
			light_state[1] = not light_state[1]
			dataj = {"on":light_state[1]}
			req = requests.put(url + 'lights/2/state',json = dataj)
			print(req.text)


try: 
	loop = asyncio.get_event_loop()
	loop.add_reader(ser, read_and_do)

	print("ok")
	loop.run_forever()

except KeyboardInterrupt:
	print("ciao")

finally:
	loop.close()

