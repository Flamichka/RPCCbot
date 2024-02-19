import os
import re
import urllib.parse
from PIL import ImageGrab
from io import BytesIO
from bot_logic import bot, ALLOWED_USER_ID
from aiogram import types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def start_command(message: types.Message):
    await message.reply(f"placeholder")

async def chrome(message, url_or_search=None):
    if url_or_search == None:
            await message.reply(f'''Поддерживет прямое открытие ссылок содержащих "http://", "https://", "ftp://", "ftps://"\nИли текстовый запрос в поисковую систему Google''')
            return
    if is_valid_url(url_or_search):
        command = f"start chrome {url_or_search}"
        os.system(command)
        await message.reply(f"Chrome запущен с URL: {url_or_search}")
    else:
        search_query = urllib.parse.quote(url_or_search)
        search_url = f"https://www.google.com/search?q={search_query}"
        command = f"start chrome {search_url}"
        os.system(command)
        await message.reply(f"Не удалось определить валидный URL. Выполнен поиск: {url_or_search}")

def is_valid_url(url):
    url_pattern = re.compile(
        r'^(?:http|ftp)s?://',  # http:// or https:// or ftp:// or ftps://
        re.IGNORECASE)
    return re.match(url_pattern, url)

async def cancelShutDown(message):
    command = "shutdown /a"
    os.system(command)
    await message.reply("Отменено")

async def shutDown(message):
    command = "shutdown /s /f /t 300"
    os.system(command)
    await message.reply("Выключение ПК")

async def screenshot(message):
    screenshot = ImageGrab.grab(all_screens = True)
    screenshot_bytes = BytesIO()
    screenshot.save(screenshot_bytes, format="PNG")
    screenshot_bytes.seek(0)
    
    await message.reply("Снимок экрана сделан. Отправляю...")
    await bot.send_photo(chat_id=message.from_user.id, photo=screenshot_bytes)

async def searchFile(message, path):
    try:
        items = os.listdir(path)
        item_count = len(items)
        
        if item_count == 0:
            await message.reply("No items found.")
            return
        
        current_index = 0
        while current_index < item_count:
            keyboard = InlineKeyboardMarkup()
            remaining_items = items[current_index:current_index+32]
            
            for item in remaining_items:
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    callback_data = f"folder_{item_path}"
                else:
                    callback_data = f"file_{item_path}"
                button_text = f"📂: {item}" if os.path.isdir(item_path) else f"🗒️: {item}"
                
                # Check if item length is greater than 60 characters
                if len(button_text) <= 50:
                    keyboard.add(InlineKeyboardButton(text=button_text, callback_data=callback_data))
            
            if current_index == 0:
                await message.reply(f"Путь {path}", reply_markup=keyboard)
            else:
                await message.reply(f"___[ ⏫ ]___", reply_markup=keyboard)
            
            current_index += 32
    except OSError as e:
        await message.reply(f"Error: {e}")



