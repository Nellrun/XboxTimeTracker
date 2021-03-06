import os
from urllib.parse import urljoin


TOKEN = os.getenv('TELEGRAM_TOKEN', '')

WEBHOOK_HOST = f'https://minecraft-nocovid19-bot.herokuapp.com/'  # Enter here your link from Heroku project settings
WEBHOOK_URL_PATH = '/webhook/' + TOKEN
WEBHOOK_URL = urljoin(WEBHOOK_HOST, WEBHOOK_URL_PATH)


WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.environ.get('PORT')


XBOX_CLIENT_ID = os.getenv('XBOX_CLIENT_ID', '')
XBOX_CLIENT_SECRET = os.getenv('XBOX_CLIENT_SECRET', '')
XBOX_TOKEN = os.getenv('XBOX_TOKEN', '{}')


DATABASE_URL = os.getenv('DATABASE_URL', '')
