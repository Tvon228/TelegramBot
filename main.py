import telebot 
import json
import redis
import requests
from telebot import types


client = redis.Redis(host='localhost',port = '6379')


API = '20b74570651857d0345293c7590f78d8'
bot = telebot.TeleBot('6416910414:AAEZjmSAP-nJndDkGUS4UePUXTIlzVsM5jE')
file = open('./Raspisanie.xlsx','rb')



@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    client.set(user_id,'default') 
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    btn1 = types.KeyboardButton('Расписание')
    btn2 = types.KeyboardButton('Погода')
    client.set(user_id,'Weather')
    btn3 = types.KeyboardButton('Курс валют')
    markup.add(btn1,btn2,btn3)
    btn4 = types.KeyboardButton('Я передумал!')
    markup.add(btn4)
    bot.send_message(message.from_user.id,f'Привет,{message.from_user.first_name}.Что тебя интересует?',reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_types(message):
        user_id = message.from_user.id
        if message.text == "Расписание":
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            mat = types.KeyboardButton('Мат 01.03.01')
            pm = types.KeyboardButton('ПМ 01.03.03')
            pmi = types.KeyboardButton('ПМИ 01.03.02')
            markup.add(mat,pm,pmi)
            back = types.KeyboardButton('Вернуться назад!')
            markup.add(back)
            bot.send_message(user_id,'Выбери свое направление:',reply_markup=markup)
        elif message.text == 'Мат 01.03.01':
            bot.send_document(user_id,file)
        elif message.text == 'ПМ 01.03.03':
            bot.send_document(user_id,file)
        elif message.text == 'ПМИ 01.03.02':
            bot.send_document(user_id,file)
        elif message.text == 'Вернуться назад!':
            bot.send_message(message.from_user.id,'Вы вернулись в главное меню!',reply_markup=markup)
            start()
        elif message.text == 'Погода':
            client.set(user_id,'Weather')
        if client.get(user_id) == b'Weather':
            print(message.text)
            bot.send_message(user_id,'Напиши свой город: ')
            city = message.text.strip().lower()
            res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
            bot.reply_to(message,f'Ам-ням говорит,что сейчас {res.json()}')



    


bot.polling(non_stop = True,interval = 0,timeout=123)