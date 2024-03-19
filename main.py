import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from database import Database, show_course_name
from keyboard_buttun import (menu_keyboard, about_keyboard, category_keyboard,
                             dasturlash_keyboard, dizayn_keyboard, marketing_keyboard)
from inline_buttun import keyword

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
        await message.answer(f"Salom @{username}", reply_markup=menu_keyboard)

    else:
        print(f"{message.from_user.username} start bot")
        query = f"""INSERT INTO users(fname, lname, username, chat_id) VALUES('{first_name}', '{last_name}', '{username}', {chat_id})"""
        print(f"{username} {Database.connect(query, "insert")} database")
        await message.answer(f"Salom @{username}", reply_markup=menu_keyboard)


@dp.message_handler(commands=["users"])
async def show_user(message: types.Message):
    data = ""

    if message.from_user.id in [1504360843, 2095041544]:  # adminlarni chat_idlari
        user_name = Database.connect(f"""SELECT fname FROM users""", "select")

        for i in user_name:
            data += f"=> {i[0]}\n"

    else:
        data += "Siz admin emassiz"

    await message.reply(data, reply_markup=menu_keyboard)


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
            Familiyangiz: Siz familiyangizni 
            kiritmagansiz""")
    else:
        await message.reply(f"""
            Salom @{data[0][3]}
            Ismingiz: {data[0][1]}
            Familiyangiz: {data[0][2]}""")


@dp.message_handler(lambda message: message.text == "Markaz haqida")
async def show_about(message: types.Message):
    await message.answer("Bo'limlardan birini tanlang:", reply_markup=about_keyboard)


@dp.message_handler(lambda message: message.text == "Umumiy ma'lumotlar")
async def show_common(message: types.Message):
    query = """SELECT couse FROM about_common;"""
    data = ""
    for i in Database.connect(query, "select"):
        data += f"=> {i[0]}\n\n"
    await message.answer(data)


@dp.message_handler(lambda message: message.text == "Afzalliklar")
async def show_advantage(message: types.Message):
    query = """SELECT advantage FROM about_advantage;"""
    data = ""
    for i in Database.connect(query, "select"):
        data += f"=> {i[0]}\n\n"
    await message.answer(data)


@dp.message_handler(lambda message: message.text == "🔙back")
async def back_main(message: types.Message):
    await message.answer(message.text, reply_markup=menu_keyboard)


@dp.message_handler(lambda message: message.text == "Yutuqlar")
async def award(message: types.Message):
    data = """
    📊 Shu kungacha kurslarni muvaffaqiyatli bitirganlar soni: 3000+

    🔥 Shu kungacha bitirgan o'quvchilarning ishga joylashishi: 70-80%
    
    🏆 2020-yilda «Yil brendi» nominatsiyasi g'olibi.
    
    🏆 2021-yilda «Eng yaxshi IT maktab» nominatsiyasi g'olibi.
    
    🎯 "Osmondagi bolalar" loyihasi muallifi.
    
    🏅 "Osmondagi bolalar" loyihasi «Tahsin» mukofoti sovrindori.
    
    🥈 YouTube kumush tugmasi.
    
    🏅 2021-yilda "Osmondagi bolalar" loyihasi «Yil kanali» deb e'tirof etildi.
    
    🎙 "Alohida mavzu" loyihasi muallifi."""
    await message.answer(data)


@dp.message_handler(lambda message: message.text == "Kurslarimiz")
async def courses(message: types.Message):
    data = Database.connect("SELECT name FROM category", "select")
    count = len(data)

    k = ""
    for i in data:
        k += f"\n=> {i[0]}\n"

    r_message = f"""
        "Najot Ta'lim" da umumiy {count} ta
    zamonaviy kasb yo'nalishi bor:\n
    {k}\n
    Bo'limlardan birini tanlang!!!
    """
    await message.answer(r_message, reply_markup=category_keyboard)


@dp.message_handler(lambda message: message.text == "Dasturlash")
async def dasturlash(message: types.Message):
    await message.answer(message.text, reply_markup=dasturlash_keyboard)


@dp.message_handler(lambda message: message.text == "Dizayn")
async def dizayn(message: types.Message):
    await message.answer(message.text, reply_markup=dizayn_keyboard)


@dp.message_handler(lambda message: message.text == "Marketing")
async def dizayn(message: types.Message):
    await message.answer(message.text, reply_markup=marketing_keyboard)


@dp.message_handler(lambda message: message.text == "<<back")
async def back_category(message: types.Message):
    await courses(message)


message_course_name = ""


@dp.message_handler(lambda message: message.text in show_course_name())
async def show_about_course(message: types.Message):
    global message_course_name
    message_course_name = message.text
    await message.answer("Tugmalarni birini tanlang", reply_markup=keyword)


@dp.callback_query_handler(text=["Skill", "Graduation", "Price"])
async def inline_answer(call: types.CallbackQuery):

    if call.data == "Skill":
        data_skill = Database.connect(f"""SELECT skill FROM courses WHERE name = '{message_course_name}';""", "select")

        await call.message.answer(f"""
        Beriladigan bilimlar:
        {data_skill[0][0]}""")

    if call.data == "Graduation":
        data_graduation = Database.connect(f"""SELECT graduation, weekly, dayly FROM courses WHERE name = '{message_course_name}';""", "select")

        await call.message.answer(f"""
        davomiyligi: {data_graduation[0][0]} oy
        haftasiga: {data_graduation[0][1]} marta
        kuniga: {data_graduation[0][2]} soat""")

    if call.data == "Price":
        data_price = Database.connect(f"""SELECT price FROM courses WHERE name = '{message_course_name}';""", "select")

        await call.message.answer(f"Kurs narxi (oyiga) {data_price[0][0]}")

    await call.answer()


@dp.message_handler(lambda message: message.text == "Filliallarimiz")
async def show_fillial(message: types.Message):
    fillial_data = (f"""
    Toshkent va Farg'ona shahrida filiallarimiz mavjud:

    📍 Chorsu 
        (https://maps.google.com/maps?q=41.325080,69.245168&ll=41.325080,69.245168&z=16)
    📍 Chilonzor 
        (https://maps.google.com/maps?q=41.285547,69.203981&ll=41.285547,69.203981&z=16)
    📍 Chimboy bekati 
        (https://maps.google.com/maps?q=41.346844,69.215791&ll=41.346844,69.215791&z=16)

    Najot Ta'lim Farg’ona filiali manzili:

    📍 Farg’ona shahar Terakmozorni orqasida Marg’ilon soy bo’yida Bolajaon parki ichida 
        (https://maps.google.com/maps?q=40.388038,71.788190&ll=40.388038,71.788190&z=16)

    Telefon raqam: 78 888 9 888""")

    await message.answer(fillial_data)


@dp.message_handler(lambda message: message.text == "Mutaxasis bilan aloqa")
async def show_aloqa(message: types.Message):
    aloqa_data = (f"""
    Tizim vaqtinchalik ish faoliyatida emas.
    
    78 888 9 888 raqami orqali bog'lanishingizni so'raymiz!""")

    await message.answer(aloqa_data)


@dp.message_handler(lambda message: message.text == "Imtihondan ro'yhatdan o'tish")
async def show_imtihon(message: types.Message):
    imtihon_data = (f"""
    Dasturlash intensiv kursiga ro'yxatdan o'tishdan oldin ushbu havola orqali kurs haqida tanishib chiqishingizni so'raymiz.

    👉 https://telegra.ph/Dasturlash-kasbiy-talim-11-26""")

    await message.answer(imtihon_data)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
