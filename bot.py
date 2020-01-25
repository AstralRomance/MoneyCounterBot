import telebot
from telebot import types, apihelper

from db_setup import DataBaseWork

API_TOKEN = ''
apihelper.proxy = {'https': 'socks5://localhost:9050'}
bot = telebot.TeleBot(token=API_TOKEN, threaded='False')

db = DataBaseWork()

keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
btn1 = types.KeyboardButton('/Мой баланс')
keyboard.add(btn1)


@bot.message_handler(commands=['Получено', 'Потрачено'])
def get_or_spend_money(message):
    tmp = message.text.split()
    if tmp[0] == '/Получено' and float(tmp[1]) >= 0:
        db.add_or_spend_money(message.chat.id, float(tmp[1]), True)
        bot.send_message(message.chat.id, text=f'Внесено {tmp[1]} рэбэлсов')
    elif tmp[0] == '/Потрачено' and float(tmp[1]) >= 0:
        db.add_or_spend_money(message.chat.id, float(tmp[1]), False)
        bot.send_message(message.chat.id, text=f'Потрачено {tmp[1]} рэбэлсов')
    else:
        bot.send_message(message.chat.id, text='Плохое (не) число', reply_markup=keyboard)


@bot.message_handler(commands=['Мой баланс'])
def get_my_balance(message):
    bot.send_message(message.chat.id, text=f'Ваш текущий баланс {db.get_balance(message.chat.id)} рэбэлсов',
                     reply_markup=keyboard)


while True:
    bot.polling(none_stop=True)