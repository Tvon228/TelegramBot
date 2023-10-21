import requests
from bs4 import BeautifulSoup

from keyboards import delete_keyboard, return_keyboard, shedule_menu_keyboard, rate_menu_keyboard   

Math = open(r"/home/perunov_vadim/ Projects/amnyam-bot/Math.xlsx",'rb')
Pm = open(r"/home/perunov_vadim/ Projects/amnyam-bot/PMPMI.xlsx",'rb')
Pmi = open(r"/home/perunov_vadim/ Projects/amnyam-bot/PMPMI.xlsx",'rb')

def default_handler(user_id, text, chat_id, redis, bot):
    if text == "Погода":
        redis.set(user_id, "weather")
        bot.send_message(chat_id, "Отправь название города, в котором хочешь узнать погоду", reply_markup=return_keyboard())

    if text == "Расписание":
        redis.set(user_id, "shedule")
        bot.send_message(chat_id,'Выбери направление:',reply_markup=shedule_menu_keyboard())
        
    if text == "Курс валют":
        redis.set(user_id, "rate")
        bot.send_message(chat_id,'Выбери валюту',reply_markup=rate_menu_keyboard())


def weather_handler(user_id, text, chat_id, redis, bot, api_key):
    redis.set(user_id, "default")
    
    city = text.strip().title()
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric')
    weather = response.json()

    try:
        temperature = weather.get("main").get("temp")
        bot.send_message(chat_id, f'Ам-ням говорит, что сейчас в городе {city} , {temperature}°C', reply_markup=return_keyboard())
    except:
        bot.send_message(chat_id, "Ам-няму не удалось найти погоду :(", reply_markup=return_keyboard())


def shedule_handler(user_id, text, chat_id, redis, bot):
    redis.set(user_id, 'default')

    if text == "МАТ👑":
        #отправить файл мат
        bot.send_document(chat_id, Math, reply_markup=return_keyboard())
        return
    elif text == "пм":
        #отправить файл пм
        bot.send_document(chat_id, Pm, reply_markup=return_keyboard())
        return
    elif text == "пми":
        #отправить файл пми
        bot.send_document(chat_id, Pmi, reply_markup=return_keyboard())
        return
    else:
        bot.send_message(chat_id, "Ам-ням тебя не понял, выбери пожалуйста существующее направление", reply_markup=shedule_menu_keyboard())

def course_handler(user_id, text, chat_id, redis, bot, URLusd, URLeur, headers):
    redis.set(user_id, 'default')
    
    usd = requests.get(URLusd, headers=headers)
    eur = requests.get(URLeur, headers=headers)
    soupusd = BeautifulSoup(usd.text, "lxml")
    soupeur = BeautifulSoup(eur.text, "lxml")
    rateUSD = soupusd.find("span", {'class' : "DFlfde SwHCTb"}).text
    rateEUR = soupeur.find("span", {'class' : "DFlfde SwHCTb"}).text

    if text == 'USD':
        bot.send_message(chat_id, f'Ам-ням не доволен,что 1 USD = {rateUSD} руб', reply_markup=return_keyboard())
    elif text == 'EUR':
        bot.send_message(chat_id, f'Ам-ням не доволен,что 1 EUR = {rateEUR} руб', reply_markup=return_keyboard())
    else:
        bot.send_message(chat_id,'Ам-ням тебя не понял!', reply_markup=rate_menu_keyboard())
    