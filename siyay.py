import asyncio
import random
import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = "8624800637:AAFmjnVUEiV_Ts6cdAZNO1VyG4idGFnJnGQ"  # Твой токен
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Список фраз для поддержки
PHRASES = [
    "у тебя получится",
    "Я верю в тебя.",
    "ты справишься.",
    "Ты не один",
    "Ты сильнее, чем думаешь.",
    "отдых — часть работы.",
    "я горжусь тобой.",
    "не забывай про отдых"
]

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Привет! Я бот «Сияй». Я помогу тебе с планами и поддержкой. 💙\n\n"
        "Вот что я умею:\n"
        "/start — показать это сообщение\n"
        "/plan — записать план на день\n"
        "/done — отметить выполненное\n"
        "/mikes — посмотреть баланс маек\n"
        "/show – посмотреть планы на день\n"
        "/help — помощь\n\n"
        "Напиши /plan, чтобы начать!"
    )
    asyncio.create_task(daily_message(message.chat.id))

async def daily_message(chat_id):
    while True:
        now = datetime.datetime.now()
        if now.hour == 15 and now.minute == 0:
            phrase = random.choice(PHRASES)
            await bot.send_message(chat_id, phrase)
            await asyncio.sleep(60)
        await asyncio.sleep(30)

# Словарь для хранения планов (chat_id -> список дел)
user_plans = {}

@dp.message(Command("plan"))
async def plan(message: types.Message):
    await message.answer("Напиши, что ты планируешь...")


@dp.message(Command("done"))
async def done(message: types.Message):
    await message.answer("Молодец! Ты выполнил дело. +2 майки! 💙")

@dp.message(Command("show"))
async def show_plans(message: types.Message):
    chat_id = message.chat.id
    if chat_id in user_plans and user_plans[chat_id]:
        plans = "\n".join([f"— {p}" for p in user_plans[chat_id]])
        await message.answer(f"Твои планы на день:\n{plans}")
    else:
        await message.answer("У тебя пока нет планов. Напиши /plan, чтобы добавить.")

@dp.message()
async def handle_plan(message: types.Message):
    if not message.text.startswith("/"):
        chat_id = message.chat.id
        if chat_id not in user_plans:
            user_plans[chat_id] = []
        user_plans[chat_id].append(message.text)
        await message.answer(f"Записал: {message.text}. Ты справишься!💙")

@dp.message(Command("done"))
async def done(message: types.Message):
    await message.answer("Молодец! Ты выполнил дело. +2 майки! 💙")

@dp.message(Command("mikes"))
async def mikes(message: types.Message):
    await message.answer("У тебя пока 0 маек. Выполняй планы, чтобы заработать! 💙")

@dp.message()
async def handle_plan(message: types.Message):
    if not message.text.startswith("/"):
        await message.answer(f"Записал: {message.text}. Ты справишься! 💙")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
