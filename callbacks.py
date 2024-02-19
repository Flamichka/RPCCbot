
import os
from aiogram import types
from bot_logic import bot
from bot_logic import dp
import commands


async def handle_callback(callback_query: types.CallbackQuery):
    try:
        callback_data = callback_query.data
        action, item_path = callback_data.split("_", 1)  # Разбиваем callback данные
        if action == "file":
            with open(item_path, 'rb') as file:
                await bot.send_document(callback_query.from_user.id, file)
        elif action == "folder":
            await commands.searchFile(callback_query.message, item_path)
        else:
            raise ValueError(f"Unknown action: {action}")  # Обработка неизвестных действий
    except ValueError as ve:
        await bot.send_message(callback_query.from_user.id, f"ValueError: {ve} ")
    except Exception as e:
        await bot.send_message(callback_query.from_user.id, f"Error: {e} | {callback_data}")

@dp.callback_query_handler(lambda query: True)
async def on_callback_query(callback_query: types.CallbackQuery):
    await handle_callback(callback_query)