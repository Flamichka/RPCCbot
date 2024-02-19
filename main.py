import asyncio
from aiogram.utils import executor
from aiogram import types, Bot
from bot_logic import dp, bot, ALLOWED_USER_ID
import commands
import logging
from callbacks import handle_callback

command_responses = {
    '/start': (None, commands.start_command),
    '/chrome': (None, commands.chrome),
    '/cancelSD': ("Выключение ПК отменено", commands.cancelShutDown),
    '/shutdown': ("Выключение ПК через 5 min", commands.shutDown),
    '/screenshot': ("Снимок экрана отправлен.", commands.screenshot),
    '/searchfile': (None, commands.searchFile)
}



@dp.message_handler(lambda message: message.text.startswith('/'))
async def handle_commands(message: types.Message):
    if message.from_user.id == ALLOWED_USER_ID:
        command = message.get_command()
        if command in command_responses:
            args = message.text.split(maxsplit=1)
            response, command_function = command_responses[command]
            if len(args) > 1:
                await command_function(message, args[1])
            else:
                await command_function(message)
            if (response):
                await message.reply(response)
        else:
            await message.reply("Неизвестная команда.")
    else:
        await message.reply("Извините, у вас нет разрешения на доступ к этому боту.")
        await bot(message.chat.id)


@dp.callback_query_handler(lambda query: True)
async def on_callback_query(callback_query: types.CallbackQuery):
    await handle_callback(callback_query)

async def listen_console():
    while True:
        try:
            inp = await asyncio.get_event_loop().run_in_executor(None, input)
            if inp.lower() == 'q':
                logging.info("Exiting the program...")
                await dp.bot.close()
                await dp.storage.close()
                await dp.storage.wait_closed()
                asyncio.get_event_loop().stop()
                break
        except asyncio.CancelledError:
            break
                
async def main():
    await asyncio.gather(
        dp.start_polling(),
        listen_console(),
    )

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
