import sys
import asyncio
import telepot
import telepot.aio
from telepot.aio.loop import MessageLoop



async def on_chat_message(msg):

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

    # chat_id == 72007055:

    await bot.sendMessage(chat_id, "ricevuto!")


TOKEN = "488772987:AAHEmKjvQsfS5U9diAB72NieKKvKqAnl9o4"  # get token from command-line
print("Avvio il bot Telegram")
bot = telepot.aio.Bot(TOKEN)
answerer = telepot.aio.helper.Answerer(bot)

loop = asyncio.get_event_loop()

loop.create_task(bot.message_loop({'chat': on_chat_message}))

print('Loop ...')

loop.run_forever()