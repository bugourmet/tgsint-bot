import os
import logging
from telegram.ext import Updater, CommandHandler, Filters
from dotenv import load_dotenv
import modules.person.lookup as person
import modules.cars.lookup as cars


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()


def error(update, context):
    """error logger"""
    logger.error("%s caused error: %s", update, context.error)


def helpmsg(update, context):
    """Bot help function,displays help message when called"""
    update.message.reply_text("""
      *Available bot commands:*\n
      /find - Person lookup by name.
      /phone - Person lookup by phone number.
      /croreg - Lookup croatian car license plates.
      /pb - Phonebook lookup
    """, parse_mode='Markdown')


bot_token = os.environ.get("BOT_TOKEN")
allowed_users = os.environ.get("USERS").split('|')


def main() -> None:
    """Main bot function, creates the updater and registers command handlers"""
    bot = Updater(bot_token)
    users = list(map(int, allowed_users))

    dispatcher = bot.dispatcher
    dispatcher.add_error_handler(error)
    dispatcher.add_handler(CommandHandler(
        "phone", person.phone, Filters.user(user_id=users)))
    dispatcher.add_handler(CommandHandler(
        "find", person.find, Filters.user(user_id=users)))
    dispatcher.add_handler(CommandHandler(
        "pb", person.phonebook, Filters.user(user_id=users)))
    dispatcher.add_handler(CommandHandler(
        "croreg", cars.croreg, Filters.user(user_id=users)))
    dispatcher.add_handler(CommandHandler(
        "help", helpmsg, Filters.user(user_id=users)))

    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    main()
