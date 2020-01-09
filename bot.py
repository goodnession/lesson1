import datetime
import ephem
from glob import glob
import logging
from random import choice


from emoji import emojize
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


import settings


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')



def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.REQUEST_KWARGS)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user, pass_user_data = True))
    dp.add_handler(CommandHandler('planet', astrology))
    dp.add_handler(CommandHandler('rk', send_rk_pictures))
#    dp.add_handler(CommandHandler('changeEmoji', change_emoji, pass_user_data = True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data = True))
    mybot.start_polling()
    mybot.idle()


def send_rk_pictures(bot, update):
    rk_list = glob('NSFWPics/RK*.*')
    rk_pic = choice(rk_list)
    bot.send_photo(chat_id = update.message.chat_id, photo = open(rk_pic, 'rb'))


#def change_emoji(user_data):
#    if 'emoji' in user_data:
#        del user_data['emoji']
#    emoji = get_user_emoji(user_data)
#    update.message.reply_text('Готово: {}'.format(emoji))


def greet_user(bot, update, user_data):
    emoji = get_user_emoji(user_data)
    user_data['emoji'] = emoji
    greeting = ('Приветствую! {}'.format(emoji))
    my_keyboard = ReplyKeyboardMarkup([ ['/rk'] ])
    logging.info(greeting)
    update.message.reply_text(greeting, reply_markup = my_keyboard)


def talk_to_me(bot, update, user_data):
    emoji = get_user_emoji(user_data)
    user_text = 'Привет {} {}! Ты написал(а): "{}"'.format(update.message.chat.first_name, emoji, update.message.text)
    logging.info('User: %s, Chat_Id: %s, Message: %s', update.message.chat.username, update.message.chat.id,
                update.message.text)
    update.message.reply_text(user_text)


def astrology(bot, update):
    now = datetime.datetime.now()
    user_input = update.message.text.split()
    planet = user_input[1]
    date = '%i/%i/%i' % (now.year, now.month, now.day)
    planet = planet.lower()
    if planet == 'mars':
        mars = ephem.Mars(date)
        position = ephem.constellation(mars)
    update.message.reply_text(position)


def get_user_emoji(user_data):
    if 'emoji' in user_data:
        return user_data['emoji']
    else:
        user_data['emoji'] = emojize(choice(settings.USER_EMOJI), use_aliases = True)
        return user_data['emoji']


main()