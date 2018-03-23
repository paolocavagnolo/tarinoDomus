import serial
import asyncio
import json
import requests
import time

s = serial.Serial('/dev/ttyUSB0', 115200)
hueUrl = "http://192.168.1.2/api/xsNe1CZ71oiR-Awe-OBkT6E4ZcbflRyDNnx4WDsB"

homeMood = 'up' 							#up / chill / smooth
exitTrigger = False 						
rooms = [False, False, False, False, False] #soggiorno / bagno / antibagno / letto / cabina
oldRooms = [False, False, False, False, False]


def accendi( mood, stanza):
	if mood == 'up':
		ct = 153
		bri = 255
	elif mood == 'chill':
		ct = 400
		bri = 160
	elif mood == 'smooth':
		ct = 453
		bri = 20
	print("accendo!")
	payload = {'on':rooms[stanza], 'bri':bri, 'ct':ct}
	print(str(stanza))
	print(requests.put(hueUrl + "/groups/" + str(stanza) + "/action", json = payload))

def lightsHue():
	global rooms, oldRooms, homeMood

	print(rooms)
	print(oldRooms)

	for i in range(len(rooms)):
		if rooms[i] != oldRooms[i]:
			accendi( homeMood , i)


def readSerial():
	global rooms, oldRooms, homeMood

	msg = []
	inCh = s.readline().decode()
	parts = inCh.split(',')

	if (len(parts) > 5):
		idMot = int(parts[2])
		idBut = chr(int(parts[5], 16))
		idStt = chr(int(parts[6], 16))
		print(str(idMot) + "," + str(idBut) + "," + str(idStt))
		parseSerial(idMot, idBut, idStt)

		lightsHue()

		oldRooms = rooms


def parseSerial( id, but, stt ):
	global homeMood, exitTrigger, rooms

	if id == 2: #ingresso

		if but == 'a':
			if stt == '1':
				exitTrigger = True
			elif stt == '2':
				exitTrigger = False
				rooms[0] = not rooms[0]	

		elif but == 'b':
			homeMood = 'chill'
			if stt == '2':
				rooms[0] = not rooms[0]
		elif but == 'c':
			homeMood = 'smooth'
			if stt == '2' and exitTrigger == True:
				leaveHome()
				return 1
			elif stt == '2':
				rooms[0] = not rooms[0]
	
	elif id == 3:
		if but == 'a':
			if stt == '2':
				rooms[0] = not rooms[0]

		elif but == 'b':
			if stt == '2':
				rooms[2] = not rooms[2]

		elif but == 'c':
			if stt == '2':
				rooms[1] = not rooms[1]




def leaveHome():
	print("goodbay")


#

try: 
	print("run!")

	#sensorsON
	#payload = {"on":True}
	#requests.put(hueUrl + "/sensors/3/config", json = payload)
	#requests.put(hueUrl + "/sensors/7/config", json = payload)

	#check the state of the rooms
	data = requests.get(hueUrl + "/groups")
	groups = json.loads(json.dumps(data.json(), sort_keys=True))
	for g in groups:
		if groups[g]['state']['any_on']:
			rooms[int(g) - 1] = True
		else:
			rooms[int(g) - 1] = False
	oldRooms = rooms



	loop = asyncio.get_event_loop()
	loop.add_reader(s, readSerial )

	loop.run_forever()


except KeyboardInterrupt:
	print("end")
	loop.close()

finally:
	loop.close()



