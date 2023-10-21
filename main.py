import telebot 
import redis


from handlers import default_handler, weather_handler, shedule_handler, course_handler
from keyboards import main_menu_keyboard


connection = redis.Redis(host='localhost',port = '6379', decode_responses=True)


API = '20b74570651857d0345293c7590f78d8'
bot = telebot.TeleBot('6416910414:AAEZjmSAP-nJndDkGUS4UePUXTIlzVsM5jE')
URLeur = 'https://www.google.com/search?q=%D0%BA%D1%83%D1%80%D1%81+%D0%B5%D0%B2%D1%80%D0%BE+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&sca_esv=575468271&sxsrf=AM9HkKnlBoWbupvBWcPKlZyyqIfTQSln1A%3A1697907789401&ei=TQQ0ZYyVGLWowPAPv5u-kAE&oq=%D0%BA%D1%83%D1%80%D1%81+tdhj+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lp=Egxnd3Mtd2l6LXNlcnAiG9C60YPRgNGBIHRkaGog0Log0YDRg9Cx0LvRjioCCAAyCRAAGIAEGAoYKjIHEAAYgAQYCjIHEAAYgAQYCjIHEAAYgAQYCjIHEAAYgAQYCjIHEAAYgAQYCjIHEAAYgAQYCjIHEAAYgAQYCjIHEAAYgAQYCjIHEAAYgAQYCkj8JlCcBliVGHABeAGQAQCYAWCgAaUHqgECMTG4AQHIAQD4AQHCAgoQABhHGNYEGLADwgIKEAAYigUYsAMYQ8ICBhAAGAcYHsICBxAjGLECGCfCAgsQABgCGIAEGAoYKsICBxAAGA0YgATiAwQYACBBiAYBkAYK&sclient=gws-wiz-serp'
URLusd = 'https://www.google.com/search?q=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BB%D0%BB%D1%80%D0%B0&gs_lcrp=EgZjaHJvbWUqCQgCEAAYChiABDIJCAAQRRg5GIAEMgkIARAAGAoYgAQyCQgCEAAYChiABDIJCAMQABgKGIAEMgkIBBAAGAoYgAQyCQgFEAAYChiABDIJCAYQABgKGIAEMgkIBxAAGAoYgAQyCQgIEAAYChiABDIJCAkQABgKGIAE0gEINDI5OGowajeoAgCwAgA&sourceid=chrome&ie=UTF-8'
headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}


@bot.message_handler(commands=['start'])
def start(message):
	text = f'Привет, {message.from_user.first_name} .Что тебя интересует?'
	bot.send_message(message.chat.id, text, reply_markup=main_menu_keyboard())


@bot.message_handler(content_types=['text'])
def new_message(message):
	user_id = message.from_user.id
	state = connection.get(user_id)
	text = message.text
	chat_id = message.chat.id

	if text == "Назад":
		connection.set(user_id, 'default')
		bot.send_message(chat_id, "Что ты хочешь сделать?", reply_markup=main_menu_keyboard())
		return

	if state == "default" or state == None:
		default_handler(user_id, text, chat_id, connection, bot)
	elif state == "weather":
		weather_handler(user_id, text, chat_id, connection, bot, API)
	elif state == "shedule":
		shedule_handler(user_id, text, chat_id, connection, bot)
	elif state == "rate":
		course_handler(user_id, text, chat_id, connection, bot, URLusd, URLeur, headers)


bot.polling(non_stop = True,interval = 0,timeout=123)