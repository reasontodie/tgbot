import os
import json
import asyncio
import logging
import datetime as dt

import aiofiles

from aiogram import Dispatcher, Bot, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, FSInputFile

from source import Parser
from source import Database
from source import add_data_to_excel

router = Router()
database = Database()


async def read_config() -> dict:
    async with aiofiles.open('config.json', 'r', encoding='utf-8') as file:
        json_data = await file.read()
        return json.loads(json_data)


@router.message(CommandStart())
async def start_command(message: Message) -> None:
    await message.reply('Hello!\nType /get_today_statistic to get today statistic.')


@router.message(Command('get_today_statistic'))
async def get_today_statistic(message: Message) -> None:
    last_count = 0
    change = 0
    filename = f'temp_{message.from_user.id}.xlsx'
    today_rows = [item for item in database.get_data_from_db() if item[2].day == dt.datetime.now().day]
    for item in today_rows:
        total_count = item[1]
        datetime_obj = item[2]

        if change == 0 and last_count == 0:
            last_count = total_count
        elif last_count <= total_count or last_count >= total_count:
            change = total_count - last_count
            last_count = total_count

        datetime = datetime_obj.strftime("%d.%m.%Y %H:%M")
        add_data_to_excel(filename, datetime, total_count, change)

    rows = FSInputFile(filename, filename=filename)
    await message.answer_document(rows)
    os.remove(filename)


async def parse_every_hour() -> None:
    parser = Parser(database)
    while True:
        now = dt.datetime.now()
        config = await read_config()
        if config['at_00:00'] is True:
            if now.minute == 0 and now.second == 0:
                await parser.parse_and_save(config['parsing_keyword'], now)
                await asyncio.sleep(1)
        else:
            await parser.parse_and_save(config['parsing_keyword'], now)
            await asyncio.sleep(3600)
        await asyncio.sleep(0.001)


async def on_startup() -> None:
    logging.info('Bot started.')
    asyncio.create_task(parse_every_hour())


async def main() -> None:
    config = await read_config()
    bot = Bot(token=config['bot_token'])
    dp = Dispatcher()
    dp.include_router(router)
    dp.startup.register(on_startup)
    await bot.delete_webhook(True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
