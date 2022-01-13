from requests.api import head
from requests.models import Response
from telegram import Update, message, update
from telegram.ext import Updater, CommandHandler,Filters, CallbackContext
import logging
import re
import requests
import json
from telegram.ext.filters import DataDict
import whois
import shodan

import config as cfg

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
                if len(joined_string) > 4096: #Split the message if it's too big(max chars in telegram is 4096)
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
        "APIKEY": cfg.SCTRAILS_API_KEY
        }
    
    reply = ''
    domains = []
    response = requests.request("GET", url, headers=headers)
    json_data = json.loads(response.text)
    
    for domain in json_data['subdomains']:
        domains.append(domain + '.' + context.args[0])
        reply = '\n'.join(domains)
    update.message.reply_text(('FOUND '+ str(json_data['subdomain_count']) + ' DOMAINS :') + '\n'+ reply)


def who(update: Update, context: CallbackContext) -> None:
    w = whois.whois(context.args[0])
    update.message.reply_text(w.text)


def shodansearch(update: Update, context: CallbackContext) -> None:
    try:
        reply = ''
        vulns = []
        ports = []
        url = 'https://api.shodan.io/dns/resolve?hostnames=' + context.args[0] + '&key=' + cfg.SHODAN_API_KEY

        response = requests.get(url)
        IP = response.json()[context.args[0]]
        api = shodan.Shodan(cfg.SHODAN_API_KEY)
        host = api.host(IP)
        if host.get('vulns') != None:
            for item in host.get('data'):
                ports.append(item['port'])
        else:
            ports.append(0)

        if host.get('vulns') != None:
            for item in host.get('vulns'):
                vulns.append(item)
                reply = '\n'.join(vulns)
        else:
            reply = ('NO CVE DATA!')
        update.message.reply_text('TARGET IP: ' + str(IP) + '\n\n' + 'CVE: ' + '\n\n' + reply + '\n\n' + 'PORTS: ' + str(ports))

    except(shodan.APIError,TypeError,KeyError) as e:
        update.message.reply_text(str(e))


def help(update, context):
    update.message.reply_text('Usage: /command <query>' + '\n' + 'Available commands:' + '\n' + '/find - Search trough sample.txt' + '\n' + '/sub - Check for subdomains' + '\n' + '/whois - Get domain WHOIS info' + '\n' + '/shodan - Scan the target using shodan.')

def main() -> None:
    # Create the updater and pass it your bot's token.
    bot = Updater(cfg.BOT_TOKEN)
    
    # Get the dispatcher to register handlers.
    dispatcher = bot.dispatcher
    dispatcher.add_handler(CommandHandler("find", search, Filters.user(user_id=cfg.users)))
    dispatcher.add_handler(CommandHandler("domains", subdomains, Filters.user(user_id=cfg.users)))
    dispatcher.add_handler(CommandHandler("whois", who, Filters.user(user_id=cfg.users)))
    dispatcher.add_handler(CommandHandler("shodan", shodansearch, Filters.user(user_id=cfg.users)))
    dispatcher.add_handler(CommandHandler("help", help))

    # Start the bot.
    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    main()
