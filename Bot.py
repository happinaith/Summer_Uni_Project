import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from Vacancy_findcomm import *

TOKEN = "7251236153:AAH1zGT_oTpH8X7n31pYqzhzXbpeFAWe1nc"

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(TOKEN)

    dp.include_router(router)

    @dp.message(Command("start"))
    async def cmd_start(message: types.Message):
        await message.answer(f"Привет! Воспользуйся коммандой /Find для парсинга вакансии")

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())