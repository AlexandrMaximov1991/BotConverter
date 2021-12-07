import telebot
from Config import keys, TOKEN
from Extensions import ConvertionExeption, ValuesConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['help'])
def message_help(message: telebot.types.Message):
    text = f'<имя валюты, цену которой вы хотите узнать> ' \
           f' <имя валюты, в которой надо узнать цену первой валюты> ' \
           f' <количество первой валюты>'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Имеющиеся валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(commands=['start'])
def message_start(message: telebot.types.Message):
    text = f'Приве, этот бот умеет конвертировать \n' \
           f'деревянный Белорусский рубль,\n' \
           f'Доллар США, Евро, Российский рубль,\n' \
           f'Эфир, Биткоин, Польский Злотый\n' \
           f'подробнее вы узнаете по команде:  values'
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionExeption('Заданы не правильные параметры!')

        quote, base, amount = values
        total_base = ValuesConverter.convert(quote, base, amount)

    except ConvertionExeption as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать вашу команду!\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base} '
        bot.send_message(message.chat.id, text)


bot.polling()
