import telebot
from config import keys, TOKEN
from extensions import CriptoConverter, APIException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = "Чтобы начать работу, введите команду боту в следующем формате:\n<имя валюты, цену которой вы хотите узнать> \
<в какой валюте измерять первую><количество переводимой валюты>\nУвидеть список всех доступных валют: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Неправильное число параметров')

        quote, base, amount = values
        total_base = CriptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        text = f'{amount} {quote} = {total_base} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()