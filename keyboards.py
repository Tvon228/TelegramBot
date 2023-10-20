from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def create_line(markup, names):
    buttons = []

    for button_name in names:
        buttons.append(KeyboardButton(button_name))

    markup.add(*buttons)

    return markup


def main_menu_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard = True)
    markup = create_line(markup, ['Расписание', 'Погода', 'Курс валют'])
    return markup


def delete_keyboard():
    return ReplyKeyboardRemove()


def return_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard = True)
    markup = create_line(markup, ['Назад'])
    return markup