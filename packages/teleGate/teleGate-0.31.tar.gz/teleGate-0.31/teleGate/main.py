import asyncio
from bot import prepareClient, Bot
from subscribers import SubscribersDefault
from api import ApiV1

import config

from version import __version__  # noqa: F401

def main():
   loop=asyncio.get_event_loop()

   client=prepareClient(
      config.TG_NAME,
      config.TG_API_ID,
      config.TG_API_HASH,
      config.TG_TOKEN,
      config.TG_PROXY,
      loop=loop,
   )

   subscribers=SubscribersDefault(filePath=config.SUBSCRIBERS_FILE)
   bot=Bot(client, subscribers)
   api=ApiV1(client, subscribers)

   bot.init()
   api_handler=api.init()

   loop.run_until_complete(loop.create_server(
      api_handler,
      host=config.API_HOST,
      port=config.API_PORT,
      backlog=config.API_BACKLOG_SIZE,
   ))
   print('Runned..')
   loop.run_forever()

if __name__ == '__main__':
   main()
