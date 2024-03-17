from db import Database
from aiogram import types

keyword = types.InlineKeyboardMarkup()
keyword.add(types.InlineKeyboardButton(text="Bilimlar", callback_data="skill"), types.InlineKeyboardButton(text="davomiyligi", callback_data="graduation"))
keyword.add(types.InlineKeyboardButton(text="Narxi", callback_data="price"))

