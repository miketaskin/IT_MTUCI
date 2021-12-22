import telebot
import datetime

from datetime import date, timedelta
from telebot import types
from db import conn, cur

token = "2110500946:AAF9DQlA1nqbbYKJzDQDFJEV1Cxj4ULTQBA"

bot = telebot.TeleBot(token)

@bot.message_handler(commands=["start"])
def start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('/понедельник', '/вторник', '/среда', '/четверг', '/пятница', '/суббота', '/чёт', '/нечёт')
    bot.send_message(message.chat.id, 'Выберите день или неделю', reply_markup=keyboard)




time = ['. 09:30-11:05 ', '. 11:20-12:55 ', '. 13:10-14:45 ', '. 15:25-17:00 ', '. 17:15-18:50 ']
day = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']

@bot.message_handler(content_types=["text"])
def answer(message):
    chetnost = delta_func()
    if message.text.lower() == "/понедельник":
        number_start, number_end = 1 + chetnost, 5 + chetnost
    elif message.text.lower() == "/вторник":
        number_start, number_end = 6 + chetnost, 10 + chetnost
    elif message.text.lower() == "/среда":
        number_start, number_end = 11 + chetnost, 15 + chetnost
    elif message.text.lower() == "/четверг":
        number_start, number_end = 16 + chetnost, 20 + chetnost   
    elif message.text.lower() == "/пятница":
        number_start, number_end = 21 + chetnost, 25 + chetnost
    elif message.text.lower() == "/суббота":
        number_start, number_end = 26 + chetnost, 30 + chetnost 
    elif message.text.lower() == "/чёт":
        number_start, number_end = 1 , 30
    elif message.text.lower() == "/нечёт":
        number_start, number_end = 31 , 60
    try:
        cur.execute(f"SELECT * FROM raspisanie WHERE id >= {number_start} AND id <= {number_end};")
        classes_array = [tuple_class[1] for tuple_class in cur.fetchall()]
        all_day_string = ''
        for i, class_name in enumerate(classes_array):
            if number_end - number_start == 29 and i % 5 == 0:
                all_day_string += '\n' + day[i//5] + '\n' + '\n' 
            if class_name != 'None':
                all_day_string += str(i%5+1) + time[i%5] +  class_name + '\n' 
        if not all_day_string:
            all_day_string = 'в этот день нет пар'
        bot.send_message(message.chat.id, all_day_string)
    except BaseException as e:
        print(e)
        pass


@bot.message_handler(content_types=["text"])
def week(message):
    bot.send_message(message.chat.id, "Я умею...")


def delta_func():
    first_day = date(2021, 8, 30)
    today = date.today()
    delta = (today - first_day).days
    chetnost = ((delta // 7) + 1) % 2
    return 0 if chetnost else 30

bot.infinity_polling()

