import requests

from keyboards import delete_keyboard, return_keyboard, main_menu_keyboard,raspisanie_menu_keyboard

def default_handler(user_id, text, chat_id, redis, bot):
    if text == "Назад":
        bot.send_message(chat_id, "Что ты хочешь сделать?", reply_markup=main_menu_keyboard())

    if text == "Погода":
        redis.set(user_id, "weather")
        bot.send_message(chat_id, "Отправь название города, в котором хочешь узнать погоду", reply_markup=delete_keyboard())

    if text == "Расписание":
        redis.set(user_id,"raspisanie")


def weather_handler(user_id, text, chat_id, redis, bot, api_key):
    city = text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric')
    redis.set(user_id, "default")
    bot.send_message(chat_id, f'Ам-ням говорит,что сейчас {res.json()}', reply_markup=return_keyboard())

def raspisanie_handler(redis,user_id):
    redis.set(user_id,'default')