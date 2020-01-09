import datetime
import ephem
from glob import glob
import logging
from random import choice


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


import settings


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')



def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.REQUEST_KWARGS)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('planet', astrology))
    dp.add_handler(CommandHandler('rk', send_rk_pictures))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    mybot.start_polling()
    mybot.idle()


def send_rk_pictures(bot, update):
    rk_list = glob('NSFWPics/RK*.*')
    rk_pic = choice(rk_list)
    bot.send_photo(chat_id = update.message.chat_id, photo = open(rk_pic, 'rb'))


def greet_user(bot, update):
    greeting = ('Приветствую!')
    logging.info(greeting)
    update.message.reply_text(greeting)


def talk_to_me(bot, update):
    user_text = 'Привет {}! Ты написал(а): "{}"'.format(update.message.chat.first_name, update.message.text)
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


main()