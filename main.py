import telebot
import config
import os, os.path, datetime
from telebot import types
bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def welcome(message):

    if os.path.exists(f'player/{message.chat.id}.txt') == False:
        open(f'player/{message.chat.id}.txt','w+')

    sti = open('sticker/sticker.webp', 'rb')
    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Добавити")
    item2 = types.KeyboardButton("Історія")
    item3 = types.KeyboardButton('Аналювати рахунок')
    item4 = types.KeyboardButton('Забрати')
    markup.add(item1,item2,item3,item4)
    bot.send_message(message.chat.id,
                     "Доброго вечора {0.first_name}!\nМи з України!".format(message.from_user,
                                                                                             bot.get_me()),
                     parse_mode="html", reply_markup=markup)
    bot.send_sticker(message.chat.id, sti)
    sti.close()

@bot.message_handler(content_types=['text'])
def lalala(message):

        if message.text == 'Добавити':
            msg = bot.send_message(message.chat.id,'Скільки хочете добавити грошей?:\nPS Потрібно вводити просто числа наприклад:200')
            bot.register_next_step_handler(msg,add)
        elif message.text == 'Історія':

            history(message)

        elif message.text == 'Аналювати рахунок':
            msg = bot.send_message(message.chat.id,'Ви точно впевнені в цьому? Напишіть так якщо впевнені: ')
            bot.register_next_step_handler(msg,analu)
        elif message.text == 'Забрати':
            msg = bot.send_message(message.chat.id,
                                   'Скільки хочете забрати грошей?:\nPS Потрібно вводити просто числа наприклад:200')
            bot.register_next_step_handler(msg, rem)
def add(message):
    try:
        messages = int(message.text)
        date = datetime.datetime.now()
        date = str(date).split()
        date = date[0]
        date=date.replace("'", "").replace("[","").replace("]",'')
        with open(f'player/{message.chat.id}.txt', 'a+',encoding='utf-8') as file:
            file.write(f'\n{date} {messages} грн')

    except:
        bot.send_message(message.chat.id,'Ви ввели неправильно')
def analu(message):
    if message.text == 'Так' or message.text == 'так':
        with open(f'player/{message.chat.id}.txt','w+'):
            bot.send_message(message.chat.id,'Історію очищено')
def rem(message):
    try:
        messages = int(message.text)

        date = datetime.datetime.now()
        date = str(date).split()
        date = date[0]
        date=date.replace("'", "").replace("[","").replace("]",'')
        with open(f'player/{message.chat.id}.txt', 'a+',encoding='utf-8') as file:
            file.write(f'\n{date} -{messages} грн')

    except:
        bot.send_message(message.chat.id,'Ви ввели неправильно')
def history(message):
    try:
        number = ''
        history = ''
        read = open(f'player/{message.chat.id}.txt', 'r+', encoding='utf-8')
        reads = read.readlines()
        if len(reads) != 1:
            for x in range(len(reads)):
                try:
                    history += reads[x] + '\n'
                    readss = reads[x]
                    readss = readss.split(' ')
                    readsss = readss[1]
                    if x < len(reads) - 1:
                        number += readsss + '+'
                    else:
                        number += readsss
                except:pass
            bot.send_message(message.chat.id, history + f'\nУ вас зараз є {eval(number)} грн')
    except:bot.send_message(message.chat.id,'Історія поки що пуста')
bot.polling(none_stop=True, timeout=123)
