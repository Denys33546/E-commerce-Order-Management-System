import os
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

load_dotenv()

from app.handlers import router


async def main():
    # Искусственная задержка, чтобы Nginx Gateway и микросервисы успели полностью инициализироваться
    print("⏳ Ожидание запуска микросервисов бэкенда...")
    await asyncio.sleep(8)

    bot = Bot(token=os.getenv("TG_TOKEN"))
    dp = Dispatcher()
    dp.include_router(router)

    print("🤖 Telegram Bot успешно запущен в режиме интеграции с FastAPI бэкендом...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
