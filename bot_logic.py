import logging
import json
from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

API_TOKEN = config['API_TOKEN']
ALLOWED_USER_ID = config['ALLOWED_USER_ID']

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
