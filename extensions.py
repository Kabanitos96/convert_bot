import telebot
import requests
import json

info = 'Для конвертации валюты отправьте боту сообщение в следующем виде: ' \
       '\n<название валюты, цену которой вы хотите узнать><пробел>' \
       '\n<название валюты, в которой надо узнать цену первой валюты><пробел>' \
       '\n<количество первой валюты> ' \
       '\nПример: ' \
       '\nевро рубль 1' \
       '\nДля вывода названий всех доступных валют введите - /values'

values = {'доллар': 'USD', 'евро': 'EUR', 'юань': 'CNY', 'тенге': 'KZT', 'рубль': 'RUB', 'гривна': 'UAH'}


class APIexception(Exception):
    pass


class Check:
    @staticmethod
    def check_and_get_price(message: telebot.types.Message):
        if len(message.text.split()) != 3:
            raise APIexception('неверное количество вводимых данных')
        base, quote, amount = message.text.lower().split()
        if base not in values.keys() or quote not in values.keys():
            raise APIexception("данных валют нет в списке доступных /values, или неверный формат ввода /help")
        if base == quote:
            raise APIexception('одинаковые валюты не могут быть сконвертированы')
        try:
            amount = float(amount.replace(',', '.'))
        except ValueError:
            raise APIexception('неверный ввод количества конвертуремой валюты')
        base1, quote1 = values[base], values[quote]
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base1}&tsyms={quote1}')
        response_dict = json.loads(r.content)
        answer = response_dict[quote1]
        y = float(amount) * float(answer)
        return f'{amount} {base1} = {y} {quote1}'
