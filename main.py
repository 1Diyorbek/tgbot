import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from db import Database

load_dotenv()

API_TOKEN = os.getenv("TG_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    chat_id = str(message.chat.id)

    check_query = f"""SELECT * FROM users WHERE chat_id = {chat_id}"""
    if len(Database.connect(check_query, "select")) >= 1:
        await message.reply(f"Salom @{username}")

    else:
        print(f"{first_name} start bot")
        query = f"""INSERT INTO users(fname, lname, username, chat_id) VALUES('{first_name}', '{last_name}', '{username}', {chat_id})"""
        print(f"{username} {Database.connect(query, "insert")} database")
        await message.reply(f"Salom @{username}")


@dp.message_handler(commands=['data'])
async def select(message: types.Message):
    chat_id = message.chat.id
    query = f"SELECT * FROM users WHERE chat_id = {chat_id}"
    data = Database.connect(query, "select")
    print(data)

    if f'{data[0][2]}' == "None":
        await message.reply(f"""
            Salom @{data[0][3]}
            Ismingiz: {data[0][1]}
            Familiyangiz: Siz familiyangizni kiritmagansiz""")
    else:
        await message.reply(f"""
            Salom @{data[0][3]}
            Ismingiz: {data[0][1]}
            Familiyangiz: {data[0][2]}""")


@dp.message_handler()
async def back(message: types.Message):
    await message.reply(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)