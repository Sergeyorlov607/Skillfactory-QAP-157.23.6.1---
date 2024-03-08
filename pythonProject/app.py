import telebot
from config import keys, TOKEN
from extensions import Convertor, ConvertionException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help',])
def start(message: telebot.types.Message):
    text = 'Привет 👋,для конвертеции валют введите команду в формате: \n<исходная валюта> \
<валюта, в которую необходимо конвертировать> \
<количество> \
Список доступных валют:\
/values'
    bot.reply_to(message, text)

@ bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text,key, ))
    bot.reply_to(message, text)

@ bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Не соответствует кол-во параметров, \
        пожалуйста введите команду в формате: \n<исходная валюта> \
        <валюта, в которую необходимо конвертировать> \
        <количество>')
        quote, base, amount = values
        total_base = Convertor.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя. Введите корректные данные.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Неудалось обработать команду.\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()
