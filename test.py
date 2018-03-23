import asyncio
import requests
import sys
import logging
import telepot
import telepot.aio
import json

s = serial.Serial('/dev/ttyUSB0', 115200)

def serialRead():
	msg = []
	inCh = s.readline().decode()
	if (len(inCh) > 10):
		msg = inCh.split(',')

		if (len(msg) < 9):
			lights(msg)
		else:
			#stats about number of times button pressed
			records(msg)

#global variables
test_text = open('test.json', 'r').read()
test_obj = json.loads(test_text)
num_lights_reacheable = 0

for x in range(0, len(test_obj['lights'])):
	if (test_obj['lights'][str(x+1)]['state']['reachable'] == True):
		num_lights_reacheable = num_lights_reacheable + 1

print(num_lights_reacheable)

#################################################


async def on_chat_message(msg):

	content_type, chat_type, chat_id = telepot.glance(msg)
	
	if content_type != 'text':
		return

	command = msg['text']
	chat_id = msg['chat']['id']

	notizia = "sono vivo! programmami, please"

	if chat_id == 72007055:
		await bot.sendMessage(chat_id, notizia)

	


def got_stdin_data(q):
	asyncio.async(q.put(sys.stdin.readline()))
	asyncio.ensure_future(myCoroutine())

async def myCoroutine():
	process_time = int(await q.get())
	req = requests.get('https://api.github.com/users/tater/events')
	print(req.status_code)

#logging
logging.basicConfig(filename='tarinoInfo.log', level=logging.INFO, format='%(asctime)s %(message)s')

#telegram
TOKEN = "488772987:AAHEmKjvQsfS5U9diAB72NieKKvKqAnl9o4"
logging.info("start telegram bot")
bot = telepot.aio.Bot(TOKEN)
answerer = telepot.aio.helper.Answerer(bot)


try: 
	q = asyncio.Queue()
	loop = asyncio.get_event_loop()
	loop.create_task(bot.message_loop({'chat': on_chat_message}))
	logging.info('started')
	loop.add_reader(sys.stdin, got_stdin_data, q)
	loop.run_forever()

except KeyboardInterrupt:
	print("ciao")

finally:
	loop.close()
	logging.info('finished')