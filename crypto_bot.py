from extensions import *  # info, values, APIexception, Check
from utils import TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def information(message):
    bot.send_message(message.chat.id, info)


@bot.message_handler(commands=['values'])
def value(message):
    text = 'Достуные валюты:'
    for key in values.keys():
        text = '\n'.join((text, key))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def send_value(message):
    try:
        z = Check.check_and_get_price(message)
    except APIexception as e:
        bot.send_message(message.chat.id, str(e))
    except Exception as e:
        bot.send_message(message.chat.id, f'ошибка сервера: {str(e)}')
    else:
        bot.send_message(message.chat.id, str(z))


bot.polling(none_stop=True)
