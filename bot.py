import datetime
import ephem
from glob import glob
import logging
from random import choice


from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


import settings


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')


def send_rk_pictures(bot, update):
    rk_list = glob('NSFWPics/RK*.*')
    rk_pic = choice(rk_list)
    bot.send_photo(chat_id = update.message.chat_id, photo = open(rk_pic, 'rb'), reply_markup = get_keyboard())


#def change_emoji(user_data):
#    if 'emoji' in user_data:
#        del user_data['emoji']
#    emoji = get_user_emoji(user_data)
#    update.message.reply_text('Готово: {}'.format(emoji))


def greet_user(bot, update, user_data):
    emoji = get_user_emoji(user_data)
    user_data['emoji'] = emoji
    greeting = ('Приветствую! {}'.format(emoji))
    logging.info(greeting)
    update.message.reply_text(greeting, reply_markup = get_keyboard())


def talk_to_me(bot, update, user_data):
    emoji = get_user_emoji(user_data)
    user_text = 'Привет {} {}! Ты написал(а): "{}"'.format(update.message.chat.first_name, emoji, update.message.text)
    logging.info('User: %s, Chat_Id: %s, Message: %s', update.message.chat.username, update.message.chat.id,
                update.message.text)
    update.message.reply_text(user_text, reply_markup = get_keyboard())


def astrology(bot, update):
    now = datetime.datetime.now()
    user_input = update.message.text.split()
    planet = user_input[1]
    date = '%i/%i/%i' % (now.year, now.month, now.day)
    planet = planet.lower()
    if planet == 'mars':
        mars = ephem.Mars(date)
        position = ephem.constellation(mars)
    update.message.reply_text(position, reply_markup = get_keyboard())


def get_user_emoji(user_data):
    if 'emoji' in user_data:
        return user_data['emoji']
    else:
        user_data['emoji'] = emojize(choice(settings.USER_EMOJI), use_aliases = True)
        return user_data['emoji']


def get_contact(bot, update, user_data):
    print(update.message.contact)
    update.message.reply_text('Готово {}'.format(get_user_emoji(user_data)), reply_markup = get_keyboard())


def get_location(bot, update, user_data):
    print(update.message.location)
    update.message.reply_text('Готово {}'.format(get_user_emoji(user_data)), reply_markup = get_keyboard())


def get_keyboard():
    contact_button = KeyboardButton('Прислать контакты', request_contact = True)
    location_button = KeyboardButton('Прислать координаты', request_location = True)
    my_keyboard = ReplyKeyboardMarkup([ ['/rk'], 
                                        [contact_button, location_button]
                                      ], resize_keyboard = True)
    return my_keyboard


def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.REQUEST_KWARGS)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user, pass_user_data = True))
    dp.add_handler(CommandHandler('planet', astrology))
    dp.add_handler(CommandHandler('rk', send_rk_pictures))
#    dp.add_handler(CommandHandler('changeEmoji', change_emoji, pass_user_data = True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data = True))
    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data = True))
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data = True))
    mybot.start_polling()
    mybot.idle()


main()