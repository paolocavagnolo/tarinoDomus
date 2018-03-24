import serial
import asyncio
import json
import requests
import time
import telepot
import telepot.aio
from telepot.aio.loop import MessageLoop
import configparser
import math
import datetime

config = configparser.RawConfigParser()
config.read('../data.cfg')


s = serial.Serial('/dev/ttyUSB0', 115200)
hueUrl = config.get('DEFAULT', 'hue-url') + config.get('DEFAULT', 'hue-key')

TOKEN = config.get('DEFAULT', 'token')


idMot = 1
idBut = 'a'
idStt = '1'
rooms = [False, False, False, False, False, False,False]
bri = 245
ct = 154

mx2h = [[1,1,1],[3,1,1],[3,3,1],[2,2,3],[2,2,2],[4,3,3],[4,5,5],[5,5,4],[1,1,1],[4,4,4]]
bright = [255,150,50]
colort = [154,400,454]

eventTrigger = False

async def on_chat_message(msg):

    global s

    content_type, chat_type, chat_id = telepot.glance(msg)
    print('Chat:', content_type, chat_type, chat_id)

    if content_type != 'text':
        return

    command = msg['text']
    chat_id = msg['chat']['id']
    try:
        nome = msg['from']['first_name']
    except:
        nome = "persona anonima"

    if chat_id == 72007055 or chat_id == 549198873:
      if command == "/scalda":
        s.write('R100\0'.encode())
        s.flush()
        await bot.sendMessage(chat_id, "Caldaia accesa cazzo!")

      elif command == "/spegni":
        s.write('R90\0'.encode())
        s.flush()
        await bot.sendMessage(chat_id, "Spento tutto, tutto. credo.")

      elif command == "/temp":
        data = requests.get(hueUrl + "/sensors/")
        temps = json.loads(json.dumps(data.json(), sort_keys=True))
        temp_sogg = temps['2']['state']['temperature']/100
        temp_letto = temps['6']['state']['temperature']/100

        await bot.sendMessage(chat_id, "Soggiorno: " + str(temp_sogg) + '\n' + "Letto: " + str(temp_letto))

      else:
        await bot.sendMessage(chat_id, "Non ho capito, forse sono sssstupido. O forse no, forse lo sei tu")
    else:
      await bot.sendMessage(chat_id, "Forse dovresti chiedere a Laopo di abilitarti, non credi?")

def readSerial():
  global idMot, idBut, idStt, rooms, bri, ct, f

  msg = []
  inCh = s.readline().decode()
  parts = inCh.split(',')

  
  f = None
  try:
    f = open('../log.log', 'a')
    f.write(str(datetime.datetime.now()) + ": ")
    f.write(str(inCh))

  finally:
    if f is not None:
       f.close()

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


try: 
  #check the state of the rooms
  data = requests.get(hueUrl + "/groups")
  groups = json.loads(json.dumps(data.json(), sort_keys=True))
  for g in groups:
    if groups[g]['state']['any_on']:
      rooms[int(g) - 1] = True
    else:
      rooms[int(g) - 1] = False

  
  #switch on the temp sensors
  payload = {"on":True}
  requests.put(hueUrl + "/sensors/2/config", json = payload)
  requests.put(hueUrl + "/sensors/6/config", json = payload)


  bot = telepot.aio.Bot(TOKEN)
  answerer = telepot.aio.helper.Answerer(bot)

  loop = asyncio.get_event_loop()
  loop.create_task(bot.message_loop({'chat': on_chat_message}))
  loop.add_reader(s, readSerial )


  loop.run_forever()


except KeyboardInterrupt:
  print("end")
  loop.close()
  f.close()

finally:
  loop.close()
