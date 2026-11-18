import asyncio
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
WEBAPP_URL = os.getenv("WEBAPP_URL", "").strip()

if not TOKEN:
    raise ValueError("Не найден токен в .env")

bot = Bot(token=TOKEN)
dp = Dispatcher()


def main_menu():
    rows = []
    if WEBAPP_URL.startswith("https://"):
        rows.append([InlineKeyboardButton(
            text="🛍️ Открыть REDRULL",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )])
    rows.extend([
        [InlineKeyboardButton(text="📚 Каталог", callback_data="catalog")],
        [InlineKeyboardButton(text="❤️ Избранное", callback_data="favorites")],
        [InlineKeyboardButton(text="👤 Профиль", callback_data="profile")]
    ])
    return InlineKeyboardMarkup(inline_keyboard=rows)


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "🔴 REDRULL\n\nДобро пожаловать! Откройте каталог одежды и аксессуаров.",
        reply_markup=main_menu()
    )


@dp.callback_query()
async def buttons(call):
    if call.data == "catalog":
        await call.message.edit_text(
            "📚 Каталог доступен в Mini App. Нажмите «Открыть REDRULL» в главном меню.",
            reply_markup=main_menu()
        )
    elif call.data == "favorites":
        await call.message.edit_text("❤️ Избранное находится внутри Mini App.", reply_markup=main_menu())
    elif call.data == "profile":
        await call.message.edit_text(
            f"👤 Твой профиль\n\nИмя: {call.from_user.first_name}\nID: {call.from_user.id}",
            reply_markup=main_menu()
        )
    await call.answer()


async def main():
    print("REDRULL запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
