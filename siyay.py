import asyncio
import random
import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = "8624800637:AAFmjnVUEiV_Ts6cdAZNO1VyG4idGFnJnGQ"  # Твой токен
bot = Bot(token=TOKEN)
dp = Dispatcher()

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

user_plans = {}
user_mikes = {}

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Привет! Я бот «Сияй». Я помогу тебе с планами и поддержкой. 💙\n\n"
        "Вот что я умею:\n"
        "/start — показать это сообщение\n"
        "/plan — записать план на день\n"
        "/done — отметить выполненное\n"
        "/mikes — посмотреть баланс маек\n"
        "/show — посмотреть планы на день\n"
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

@dp.message(Command("plan"))
async def plan(message: types.Message):
    await message.answer("Напиши, что ты планируешь...")

@dp.message(Command("done"))
async def done(message: types.Message):
    chat_id = message.chat.id
    if chat_id not in user_plans or not user_plans[chat_id]:
        await message.answer("У тебя нет планов. Сначала напиши /plan.")
        return
    plan_text = user_plans[chat_id].pop(0)
    if chat_id not in user_mikes:
        user_mikes[chat_id] = 0
    user_mikes[chat_id] += 2
    await message.answer(f"Молодец! Ты выполнил: «{plan_text}». +2 майки! Теперь у тебя {user_mikes[chat_id]} маек. 💙")

@dp.message(Command("mikes"))
async def mikes(message: types.Message):
    chat_id = message.chat.id
    balance = user_mikes.get(chat_id, 0)
    await message.answer(f"У тебя {balance} маек. Выполняй планы, чтобы заработать! 💙")

@dp.message(Command("show"))
async def show_plans(message: types.Message):
    chat_id = message.chat.id
    if chat_id in user_plans and user_plans[chat_id]:
        plans = "\n".join([f"— {p}" for p in user_plans[chat_id]])
        await message.answer(f"Твои планы на день:\n{plans}")
    else:
        await message.answer("У тебя пока нет планов. Напиши /plan, чтобы добавить.")

@dp.message(Command("help"))
async def help_cmd(message: types.Message):
    await message.answer(
        "Я бот «Сияй». Вот что я умею:\n"
        "/start — начать\n"
        "/plan — записать план\n"
        "/done — отметить выполненное\n"
        "/mikes — посмотреть майки\n"
        "/show — показать планы\n"
        "/help — эта справка\n\n"
        "Просто напиши мне, если нужна поддержка. 💙"
    )

@dp.message()
async def handle_plan(message: types.Message):
    if not message.text.startswith("/"):
        chat_id = message.chat.id
        if chat_id not in user_plans:
            user_plans[chat_id] = []
        user_plans[chat_id].append(message.text)
        await message.answer(f"Записал: {message.text}. Ты справишься! 💙")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
