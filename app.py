import os
from urllib.parse import urljoin

import aiohttp
# from aiohttp import web
from aiogram import Bot, Dispatcher, types
# from aiogram.utils import context
# from aiogram.dispatcher.webhook import get_new_configured_app

TOKEN = os.getenv('TOKEN', '')

WEBHOOK_HOST = f'https://minecraft-nocovid19-bot.herokuapp.com/'  # Enter here your link from Heroku project settings
WEBHOOK_URL_PATH = '/webhook/' + TOKEN
WEBHOOK_URL = urljoin(WEBHOOK_HOST, WEBHOOK_URL_PATH)


WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.environ.get('PORT')

bot = Bot(TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    """Handle start command"""
    await message.reply("I'm alive")


async def on_startup(app):
    """Simple hook for aiohttp application which manages webhook"""
    await bot.delete_webhook()
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    # insert code here to run it before shutdown
    pass


if __name__ == '__main__':
    start_webhook(dispatcher=dp, webhook_path=WEBHOOK_URL_PATH,
                  on_startup=on_startup, on_shutdown=on_shutdown,
                  host=WEBAPP_HOST, port=WEBAPP_PORT)
    # Create aiohttp.web.Application with configured route for webhook path
    # app = get_new_configured_app(dispatcher=dp, path=WEBHOOK_URL_PATH)
    # app.on_startup.append(on_startup)
    # dp.loop.set_task_factory(context.task_factory)
    # web.run_app(app, host='0.0.0.0', port=os.getenv('PORT'))  # Heroku stores port you have to listen in your app
