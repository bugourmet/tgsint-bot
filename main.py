from telegram import Update, message, update
from telegram.ext import Updater, CommandHandler,Filters, CallbackContext
import logging
import requests
import json
from telegram.ext.filters import DataDict
import whois
import shodan
from bs4 import BeautifulSoup
import config as cfg


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def search(update: Update, context: CallbackContext) -> None:
    try:
        response = requests.get("http://localhost:3000/post/" + context.args[0])
        data = []
        reply = ''
        jobjects = json.loads(response.text)
        for jobj in jobjects:
            if jobj == "error":
                update.message.reply_text("User not found!")
            else:
                #update.message.reply_text(jobj["name"])
                data.append('Phone Number: +' + str(jobj["phonenum"]))
                data.append('FB link:  https://www.facebook.com/' + str(jobj["fbid"]))
                data.append('Name: ' + jobj["name"])
                data.append('Surname: ' + jobj["surname"])
                data.append('Sex: ' + jobj["sex"])
                data.append('Extra Info: ' + str(jobj["extra"]))
                reply = '\n'.join(data)
                update.message.reply_text(reply)

    except requests.exceptions.ConnectionError as e:
        print(e)
    except requests.exceptions.RequestException as e:
        print(e)
    except KeyError as e:
        print(e)


def subdomains(update: Update, context: CallbackContext) -> None:
    try:
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
        
        if "count" in json_data:
            update.message.reply_text("No subdomains found for given domain!")
        elif (json_data["meta"]) == {"limit_reached": "True"}:
            update.message.reply_text("API requests limit reached!")
        else:
            for domain in json_data['subdomains']:
                domains.append(domain + '.' + context.args[0])
                reply = '\n'.join(domains)
            update.message.reply_text(('FOUND '+ str(json_data['subdomain_count']) + ' DOMAINS :') + '\n'+ reply)
    except requests.exceptions.ConnectionError as e:
        print(e)
    except requests.exceptions.RequestException as e:
        print(e)
    except KeyError as e:
        print(e)


def who(update: Update, context: CallbackContext) -> None:
    try:
        update.message.reply_text(whois.whois(context.args[0]))
    except:
        update.message.reply_text("Couldn't resolve!")
        

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


def bihreg(update: Update, context: CallbackContext) -> None:
    try:
        if len(context.args[0]) < 3:
            update.message.reply_text("Please enter a query longer than 3 chars.")
        else:
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:88.0) Gecko/20100101 Firefox/88.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': 'https://www.bzkbih.ba/',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Origin': 'https://www.bzkbih.ba',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-User': '?1',
                'Sec-GPC': '1',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                'TE': 'trailers',
            }

            params = (
                ('kat', '82'),
            )

            data = {
            'searchRegNr': context.args[0],
            'searchDate': '01.10.2021',
            'third_email': '',
            'action': 'doSearch',
            'mode': 'print',
            'btnSearch': 'TRAZI'
            }

            response = requests.post('https://www.bzkbih.ba/ba/stream.php', headers=headers, params=params, data=data)
            soup = BeautifulSoup(response.content, 'lxml')
            result = soup.find("td", {"colspan": "2"})
            if "vozilo se ne može pronaći" in result.text:
                update.message.reply_text("Vehicle Details Not Found!")
            else:
                update.message.reply_text(result.text)

    except requests.exceptions.ConnectionError as e:
        print(e)
    except requests.exceptions.RequestException as e:
        print(e)


def croreg(update: Update, context: CallbackContext) -> None:
    try:
        if len(context.args[0]) < 3:
            update.message.reply_text("Please enter a query longer than 3 chars.")
        else:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
                'Accept': 'application/json',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Content-Type': 'application/json',
                'Origin': 'https://kupi.laqo.hr',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Referer': 'https://kupi.laqo.hr/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site',
                'Sec-GPC': '1',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
            }

            response = requests.post('https://api.laqo.hr/webshop/ace/api/v1/car/details', headers=headers, json={'plateNumber':context.args[0]})

            data = []
            reply = ''
            jobjects = json.loads(response.text)
            if "statusCode" in jobjects:
                update.message.reply_text("Vehicle Details Not Found!")
            else:
                data.append('Istek Police: ' + str(jobjects["vehiclePolicyDetails"]["policyExpirationDate"]))
                data.append('Broj Police: ' + str(jobjects["vehiclePolicyDetails"]["policyNumber"]))
                data.append('VIN: ' + str(jobjects["vinNumber"]))
                data.append('Tip Automobila: ' + str(jobjects["vehicleType"]))
                data.append('Marka: ' + str(jobjects["vehicleManufacturerName"]))
                data.append('Model: ' + str(jobjects["model"]))
                data.append('Tip Goriva: ' + str(jobjects["fuelType"]))
                data.append('Godina Proizvodnje: ' + str(jobjects["yearOfManufacture"]))
                data.append('Boja: ' + str(jobjects["color"]))
                data.append('Snaga(kW): ' + str(jobjects["kw"]))
                reply = '\n'.join(data)
                update.message.reply_text(reply)
            
    except requests.exceptions.ConnectionError as e:
        print(e)
    except requests.exceptions.RequestException as e:
        print(e)
    except KeyError as e:
        print(e)


def help(update, context):
    update.message.reply_text("""Usage:  /command <query> \n
      Available commands:
      /find <phonenumber> - Search for a phone number info using tgsint-api.
      /domains - Check for subdomains
      /whois - WHOIS lookup
      /shodan - Scan the target using shodan.
      /bihreg <platenum> - Lookup info on bosnian car license plates.
      /croreg <platenum> - Lookup info on croatian car license plates.
    """)


def main() -> None:
    # Create the updater and pass it your bot's token.
    bot = Updater(cfg.BOT_TOKEN)
    
    # Get the dispatcher to register handlers.
    dispatcher = bot.dispatcher
    dispatcher.add_handler(CommandHandler("find", search, Filters.user(user_id=cfg.users)))
    dispatcher.add_handler(CommandHandler("domains", subdomains, Filters.user(user_id=cfg.users)))
    dispatcher.add_handler(CommandHandler("whois", who, Filters.user(user_id=cfg.users)))
    dispatcher.add_handler(CommandHandler("shodan", shodansearch, Filters.user(user_id=cfg.users)))
    dispatcher.add_handler(CommandHandler("bihreg", bihreg, Filters.user(user_id=cfg.users)))
    dispatcher.add_handler(CommandHandler("croreg", croreg, Filters.user(user_id=cfg.users)))
    dispatcher.add_handler(CommandHandler("help", help))

    # Start the bot.
    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    main()
