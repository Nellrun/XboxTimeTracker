import config
import pg
import xbox_client

from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook

bot = Bot(config.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    """Handle start command"""
    await message.reply("""
/chat_id - вывести id чата
/online - вывести текущий онлайн на сервере
/subscribe - подписаться на оповещение о заходе в игру
    """)


@dp.message_handler(commands=['online'])
async def online(message: types.Message):
    """Handle online command"""
    client = xbox_client.get_client()
    online = await client.get_minecraft_online()

    if not online:
        await message.reply('Nobody is playing minecraft =(')
    else:
        await message.reply('Players: \n' + '\n'.join(friend.gamertag for friend in online))


@dp.message_handler(commands=['chat_id'])
async def chat_id(message: types.Message):
    await message.reply(message.chat.id)


@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    pg_client = await pg.get_client()
    try:
        await pg_client.make_subscribe(message.chat.id)
    except Exception:
        await message.reply('Something went wrong')
        raise
    else:
        await message.reply('Successfully subscribed')


async def on_startup(app):
    """Simple hook for aiohttp application which manages webhook"""
    await bot.delete_webhook()
    await bot.set_webhook(config.WEBHOOK_URL)


async def on_shutdown(dp):
    await pg.close()
    await xbox_client.close()


if __name__ == '__main__':
    start_webhook(dispatcher=dp, webhook_path=config.WEBHOOK_URL_PATH,
                  on_startup=on_startup, on_shutdown=on_shutdown,
                  host=config.WEBAPP_HOST, port=config.WEBAPP_PORT)
