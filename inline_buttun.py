from database import Database
from aiogram import types

keyword = types.InlineKeyboardMarkup()
keyword.add(types.InlineKeyboardButton(text="Bilimlar", callback_data="Skill"), types.InlineKeyboardButton(text="davomiyligi", callback_data="Graduation"))
keyword.add(types.InlineKeyboardButton(text="Narxi", callback_data="Price"))

