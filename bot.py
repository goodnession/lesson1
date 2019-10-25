from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import settings


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')



def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.REQUEST_KWARGS)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me)) 
    mybot.start_polling()
    mybot.idle()


def greet_user(bot, update):
    greeting = ('Приветствую!')
    logging.info(greeting)
    update.message.reply_text(greeting)


def talk_to_me(bot, update):
    user_text = 'Привет {}! Ты написал(а): "{}"'.format(update.message.chat.first_name, update.message.text)
    logging.info('User: %s, Chat_Id: %s, Message: %s', update.message.chat.username, update.message.chat.id,
                update.message.text)
    update.message.reply_text(user_text)


main()