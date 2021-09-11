import config
import helpers
import postgres
import xbox_live

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
/stats - общая статистика по игровому времени
    """)


@dp.message_handler(commands=['online'])
async def online(message: types.Message):
    """Handle online command"""
    client = xbox_live.client.get_client()
    online_players = await client.get_online()

    if not online_players:
        await message.reply('Nobody is online =(')
    else:
        await message.reply('Players: \n' + '\n'.join(friend.gamertag for friend in online_players))


@dp.message_handler(commands=['chat_id'])
async def chat_id(message: types.Message):
    await message.reply(message.chat.id)


@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    pg_client = await postgres.client.get_client()
    try:
        await pg_client.make_subscribe(message.chat.id)
    except Exception:
        await message.reply('Something went wrong')
        raise
    else:
        await message.reply('Successfully subscribed')


@dp.message_handler(commands=['stats'])
async def stats(message: types.Message):
    pg_client = await postgres.client.get_client()
    history = await pg_client.get_history_full()

    time_by_player = helpers.calc_total_time_by_gametag(history)
    lines = helpers.format_playtime_message(time_by_player)

    message_to_reply = '*Total stats:*\n' + '\n'.join(lines)
    await message.reply(message_to_reply, parse_mode=types.ParseMode.MARKDOWN)


async def on_startup(app):
    """Simple hook for aiohttp application which manages webhook"""
    await bot.delete_webhook()
    await bot.set_webhook(config.WEBHOOK_URL)


async def on_shutdown(dp):
    await postgres.client.close()
    await xbox_live.client.close()


if __name__ == '__main__':
    start_webhook(dispatcher=dp, webhook_path=config.WEBHOOK_URL_PATH,
                  on_startup=on_startup, on_shutdown=on_shutdown,
                  host=config.WEBAPP_HOST, port=config.WEBAPP_PORT)
