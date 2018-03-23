import serial
import asyncio
import json
import requests
import time

s = serial.Serial('/dev/ttyUSB0', 115200)
hueUrl = "http://192.168.1.124/api/xsNe1CZ71oiR-Awe-OBkT6E4ZcbflRyDNnx4WDsB"

idMot = 1
idBut = 'a'
idStt = '1'
rooms = [False, False, False, False, False, False,False]
bri = 245
ct = 154

mx2h = [[1,1,1],[1,3,3],[1,3,3],[2,2,3],[2,2,2],[3,3,4],[5,5,4],[5,5,4],[1,1,1],[4,4,4]]
bright = [255,150,50]
colort = [154,400,454]

eventTrigger = False


def readSerial():
	global idMot, idBut, idStt, rooms, bri, ct

	msg = []
	inCh = s.readline().decode()
	parts = inCh.split(',')

	if (len(parts) == 8):
		idMot = int(parts[2])
		idBut = chr(int(parts[5], 16))
		if idBut == 'a':
			idBtn = 0
		elif idBut == 'b':
			idBtn = 1
		elif idBut == 'c':
			idBtn = 2
		idStt = chr(int(parts[6], 16))

		for i in range(2,12):
			if (idMot == i):
				for let in range(0,3):
					if (idBtn == let):
						x = mx2h[idMot-2][let]

						if (idStt == '1'):
							data = requests.get(hueUrl + "/groups/" + str(x))
							groups = json.loads(json.dumps(data.json(), sort_keys=True))
							rooms[x] = groups['state']['any_on']
								
						if (idStt == '2'):
							rooms[x] = not rooms[x]
							payload = {"on":rooms[x]}
							requests.put(hueUrl + "/groups/" + str(x) + "/action", json = payload)


async def presenceRead():

	data = requests.get(hueUrl + "/sensors/3")


try: 
	#check the state of the rooms
	data = requests.get(hueUrl + "/groups")
	groups = json.loads(json.dumps(data.json(), sort_keys=True))
	for g in groups:
		if groups[g]['state']['any_on']:
			rooms[int(g) - 1] = True
		else:
			rooms[int(g) - 1] = False

	#put sensors on
	requests.put(hueUrl + "/sensors/3/config", json = {"on":True})
	requests.put(hueUrl + "/sensors/7/config", json = {"on":True})

	loop = asyncio.get_event_loop()
	loop.add_reader(s, readSerial )

	task = loop.create_task(presenceRead())

	loop.run_forever()


except KeyboardInterrupt:
	print("end")
	loop.close()

finally:
	loop.close()



