from telegram import Update, update
from telegram.ext import Updater, CommandHandler,Filters, CallbackContext
import logging
import re
import requests
import json
from bs4 import BeautifulSoup
from bs4.element import ProcessingInstruction
from telegram.ext.filters import DataDict

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def search(update: Update, context: CallbackContext) -> None:
    if len(context.args[0]) < 3:
        update.message.reply_text("Please enter a query longer than 3 chars.")
    else:
        with open('sample.txt', 'r',encoding="utf-8") as file:
            count = 0
            results = []
            for line in file:
                if re.search(context.args[0],line, re.IGNORECASE):
                    count += 1
                    results.append(line)
                    
            update.message.reply_text('TOTAL MATCHES FOUND: '+ str(count))
            if count>0:
                joined_string = "\n".join(results)
                if len(joined_string) > 4096: #split the message if it's too big(max chars in telegram is 4096)
                    for x in range(0, len(joined_string), 4096):
                        update.message.reply_text(joined_string[x:x+4096])
                else:
                 update.message.reply_text(joined_string)


def subdomains(update: Update, context: CallbackContext) -> None:
    if len(context.args[0]) < 3:
        update.message.reply_text("Please enter a query longer than 3 chars.")
    else:
        url = "https://api.securitytrails.com/v1/domain/" + context.args[0] + "/subdomains?children_only=false&include_inactive=false"

    headers = {
        "Accept": "application/json",
        "APIKEY": "API_KEY"
    }
    
    reply = ''
    domains = []
    response = requests.request("GET", url, headers=headers)
    json_data = json.loads(response.text)
    
    for domain in json_data['subdomains']:
        domains.append(domain + '.' + context.args[0])
        reply='\n'.join(domains)
    update.message.reply_text(('FOUND '+ str(json_data['subdomain_count']) + ' DOMAINS :') + '\n'+ reply)



def help(update, context):
    update.message.reply_text('Usage: /command <query>' + '\n' + 'Available commands:' + '\n' + '/find - Search trough sample.txt' + '\n' + '/sub - Check for subdomains' + '\n' + '/whois - Get domain WHOIS info')



def whois(update: Update, context: CallbackContext) -> None:
   page = requests.get("https://www.iana.org/whois?q=" + context.args[0])
   soup = BeautifulSoup(page.content, 'lxml')
   data = ''
   for result in soup.find_all("pre"):
       data = data.join(result.string.strip())
   update.message.reply_text(data)



def main() -> None:

    # Create the updater and pass it your bot's token.
    bot = Updater("BOT_TOKEN")
    
    # Get the dispatcher to register handlers
    dispatcher = bot.dispatcher
    dispatcher.add_handler(CommandHandler("find", search, Filters.user(user_id=YOUR_ID))) #or use list of id's to enable multiple users to execute the command.
    dispatcher.add_handler(CommandHandler("domains", subdomains, Filters.user(user_id=YOUR_ID))) #or use list of id's to enable multiple users to execute the command.
    dispatcher.add_handler(CommandHandler("whois", whois, Filters.user(user_id=YOUR_ID))) #or use list of id's to enable multiple users to execute the command.
    dispatcher.add_handler(CommandHandler("help", help))

    # start the bot
    bot.start_polling()
    bot.idle()

if __name__ == '__main__':
    main()
