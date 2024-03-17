from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from db import Database


def add_buttun(buttun, data):
    for i in range(0, len(data), 2):
        if i != len(data) - 1:
            buttun.add(data[i][0], data[i + 1][0])
        else:
            buttun.add(data[i][0], "<<back")

    if len(data) % 2 == 0:
        buttun.add('<<back')


menu_keyboard = ReplyKeyboardMarkup(
    [
    [KeyboardButton("Markaz haqida"), KeyboardButton("Kurslarimiz")],
    [KeyboardButton("Filliallarimiz"), KeyboardButton("Mutaxasis bilan aloqa")],
    [KeyboardButton("Imtihondan ro'yhatdan o'tish")],
    ], resize_keyboard=True)


about_keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton("Umumiy ma'lumotlar"), KeyboardButton("Afzalliklar")],
        [KeyboardButton("Yutuqlar"), KeyboardButton("🔙back")]
    ],
    resize_keyboard=True)

category_keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton("Dasturlash"), KeyboardButton("Dizayn")],
        [KeyboardButton("Marketing"), KeyboardButton("🔙back")]
    ],
    resize_keyboard=True)


dasturlash_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
data_dasturlash = Database.connect("SELECT name FROM courses WHERE category_id = 1 ORDER BY course_id;", "select")
add_buttun(dasturlash_keyboard, data_dasturlash)

dizayn_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
data_dizayn = Database.connect("SELECT name FROM courses WHERE category_id = 2 ORDER BY course_id;", "select")
add_buttun(dizayn_keyboard, data_dizayn)

marketing_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
data_marketing = Database.connect("SELECT name FROM courses WHERE category_id = 3 ORDER BY course_id;", "select")
add_buttun(marketing_keyboard, data_marketing)

