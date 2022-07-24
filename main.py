from telegram.ext import Updater, CommandHandler,Filters
import logging
import os
from dotenv import load_dotenv
import modules.shodan.lookup as shodan
import modules.nmap.lookup as nmap
import modules.person.lookup as person
import modules.cars.lookup as cars
import modules.nmap.lookup as nmap


#logging.basicConfig(filename='log.txt', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv() 


def error(update, context): 
    logger.warning("%s" ' caused error: "%s"', update, context.error)
    

def help(update, context):
    update.message.reply_text("""
      *Available bot commands:*\n
      /find - Person lookup by name.
      /phone - Person lookup by phone number.
      /whois - WHOIS lookup.
      /cve - CVE scan using shodan.
      /domains - Subdomains scan. 
      /geoip - Lookup target geoip info.
      /bihreg - Lookup bosnian car license plates.
      /croreg - Lookup croatian car license plates.
      /nmap - Nmap scans.
    """,parse_mode= 'Markdown')


def main() -> None:
    # Create the updater and pass it your bot's token.
    bot = Updater(os.environ.get("BOT_TOKEN"))
    users = list(map(int, os.environ.get("USERS").split('|')))

    # Get the dispatcher to register handlers.
    dispatcher = bot.dispatcher
    dispatcher.add_error_handler(error)
    dispatcher.add_handler(CommandHandler("phone", person.phone, Filters.user(user_id=users)))
    dispatcher.add_handler(CommandHandler("whois", person.whois, Filters.user(user_id=users)))
    dispatcher.add_handler(CommandHandler("cve", shodan.cvescan, Filters.user(user_id=users)))
    dispatcher.add_handler(CommandHandler("bihreg", cars.bihreg, Filters.user(user_id=users)))
    dispatcher.add_handler(CommandHandler("croreg", cars.croreg, Filters.user(user_id=users)))
    dispatcher.add_handler(CommandHandler("find", person.find, Filters.user(user_id=users)))
    dispatcher.add_handler(CommandHandler("geoip", shodan.geoip, Filters.user(user_id=users)))
    dispatcher.add_handler(CommandHandler("domains", nmap.domains, Filters.user(user_id=users)))
    dispatcher.add_handler(CommandHandler("nmap", nmap.nmap_scan, Filters.user(user_id=users)))
    dispatcher.add_handler(CommandHandler("help", help, Filters.user(user_id=users)))

    # Start the bot.
    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    main()