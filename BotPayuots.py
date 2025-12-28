import asyncio
import sqlite3
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8309574268:AAEfunUPSaOY0aj5nwL1Dt8tR5YC-qL8fUI"
SOURCE_CHANNEL_ID = -1003541008559  # ID твоего канала
CHANNEL_LINK = "https://t.me/+O4kyMr0n_r02Y2M6"  # ссылка на канал

bot = Bot(token=TOKEN)
dp = Dispatcher()

# база пользователей
conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)"
)
conn.commit()

# клавиатура с кнопкой под постом
keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔗 BitSwap", url=CHANNEL_LINK)]
    ]
)

# Хендлер для /start
@dp.message(Command("start"))
async def start(message: Message):
    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
        (message.from_user.id,)
    )
    conn.commit()

    await message.answer(
            "🤖 Бот активирован\n\n"
            "Добро пожаловать👋\n"
            "Здесь отображается история выплат сотрудникам в USDT.\n\n"
            "📌 В этом разделе вы сможете:\n"
            "• Просматривать все совершённые выплаты\n"
            "• Отслеживать суммы и даты переводов\n"
            "• Проверять хеш (TXID) каждой USDT-транзакции\n"
            "• Контролировать прозрачную финансовую историю"
        )

# Хендлер для репоста постов с канала
@dp.channel_post()
async def repost(channel_post: Message):
    if channel_post.chat.id != SOURCE_CHANNEL_ID:
        return

    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()

    for (user_id,) in users:
        try:
            await bot.copy_message(
                chat_id=user_id,
                from_chat_id=channel_post.chat.id,
                message_id=channel_post.message_id,
                reply_markup=keyboard
            )
        except Exception as e:
            print(f"Не удалось отправить {user_id}: {e}")

# Запуск бота
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
