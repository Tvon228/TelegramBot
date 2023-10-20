import telebot 
import redis


from handlers import default_handler, weather_handler,raspisanie_handler
from keyboards import main_menu_keyboard


connection = redis.Redis(host='localhost',port = '6379', decode_responses=True)


API = '20b74570651857d0345293c7590f78d8'
bot = telebot.TeleBot('6416910414:AAEZjmSAP-nJndDkGUS4UePUXTIlzVsM5jE')
file = open('./Raspisanie.xlsx','rb')


@bot.message_handler(commands=['start'])
def start(message):
	text = f'Привет,{message.from_user.first_name}.Что тебя интересует?'
	bot.send_message(message.chat.id, text, reply_markup=main_menu_keyboard())


@bot.message_handler(content_types=['text'])
def new_message(message):
	user_id = message.from_user.id
	state = connection.get(user_id)
	text = message.text
	chat_id = message.chat.id

	if state == "default" or state == None:
		default_handler(user_id, text, chat_id, connection, bot)
	elif state == "weather":
		weather_handler(user_id, text, chat_id, connection, bot, API)
	elif state == "raspisanie":
		raspisanie_handler(user_id, chat_id, connection, bot)

bot.polling(non_stop = True,interval = 0,timeout=123)