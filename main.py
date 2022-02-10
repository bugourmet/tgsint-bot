from telegram import Update,message, update
from telegram.ext import Updater, CommandHandler,Filters, CallbackContext
import logging
import requests
import json
from telegram.ext.filters import DataDict
import whois
import shodan
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import re

#logging.basicConfig(filename='log.txt', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv() 


def find(update: Update, context: CallbackContext) -> None:
    try:
        response = requests.get(os.environ.get("API_URL") + context.args[0] + "/" + context.args[1])
        data = []
        reply = ''
        jobjects = json.loads(response.text)
        for jobj in jobjects:
            if jobj == "error":
                update.message.reply_text("User not found!")
            else:
                data.append('\nPhone Number: +' + str(jobj["phonenum"]))
                data.append('FB link:  https://www.facebook.com/' + str(jobj["fbid"]))
                data.append('Name: ' + jobj["name"])
                data.append('Surname: ' + jobj["surname"])
                data.append('Sex: ' + jobj["sex"])
                data.append('Extra Info: ' + str(jobj["extra"]))
                reply = '\n'.join(data) 
        update.message.reply_text(reply)

    except requests.exceptions.RequestException as e:
        print(e)
    except KeyError as e:
        print(e)
    except IndexError:
        update.message.reply_text("Missing argument!")


def phone(update: Update, context: CallbackContext) -> None:
    try:
        if len(context.args[0]) < 8:
            update.message.reply_text("Please enter a longer query.")
        else:
            if "+" in context.args[0]:
                context.args[0]=(context.args[0]).replace("+","")
            response = requests.get(os.environ.get("API_URL") + "api/phone/" + context.args[0])
            data = []
            reply = ''
            jobjects = json.loads(response.text)
            for jobj in jobjects:
                if jobj == "error":
                    update.message.reply_text("User not found!")
                else:
                    data.append('Phone Number: +' + str(jobj["phonenum"]))
                    data.append('FB link:  https://www.facebook.com/' + str(jobj["fbid"]))
                    data.append('Name: ' + jobj["name"])
                    data.append('Surname: ' + jobj["surname"])
                    data.append('Sex: ' + jobj["sex"])
                    data.append('Extra Info: ' + str(jobj["extra"]))
                    reply = '\n'.join(data)
                    update.message.reply_text(reply)
                    
    except requests.exceptions.RequestException as e:
        print(e)
    except KeyError as e:
        print(e)
    except IndexError:
        update.message.reply_text("Missing argument!")


def who(update: Update, context: CallbackContext) -> None:
    try:
        update.message.reply_text(whois.whois(context.args[0]))
    except IndexError:
        update.message.reply_text("Missing argument!")


def cvescan(update: Update, context: CallbackContext) -> None:
    try:
        reply = ''
        vulns = []
        ports = []
        url = 'https://api.shodan.io/dns/resolve?hostnames=' + context.args[0] + '&key=' + os.environ.get("SHODAN_API_KEY")
        response = requests.get(url)
        IP = response.json()[context.args[0]]
        api = shodan.Shodan(os.environ.get("SHODAN_API_KEY"))
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

    except requests.exceptions.ConnectionError as e:
        update.message.reply_text("Couldn't resolve! Connection error!")
    except(shodan.APIError,TypeError,KeyError):
        update.message.reply_text("Couldn't resolve  the host!")
    except IndexError:
        update.message.reply_text("Missing argument!")


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

    except requests.exceptions.RequestException as e:
        print(e)
    except IndexError:
        update.message.reply_text("Missing argument!")


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

            response = requests.post('https://api.laqo.hr/webshop/ace/api/v1/car/details', headers=headers, json={'plateNumber':(context.args[0]).upper()})

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

                month = str(jobjects["vehiclePolicyDetails"]["policyExpirationDate"]).split("-")
                data = {    
                'VIN': str(jobjects["vinNumber"]),
                'month': month[1]
                }
                response = requests.post('https://www.cvh.hr/Umbraco/Surface/TabsSurface/mot',data=data)
                jobjects = json.loads(response.text)
                exam_result = re.sub(re.compile('<.*?>') , '', str(jobjects["response"])).replace("Preuzmi u Excel formatu","")
                if len(exam_result) > 4096: #split the exam_result if it's too big(max chars/message on telegram is 4096)
                    for x in range(0, len(exam_result), 4096):
                        update.message.reply_text(exam_result[x:x+4096])
                else:
                 update.message.reply_text(exam_result)

    except requests.exceptions.RequestException as e:
        print(e)
    except KeyError as e:
        print(e)
    except IndexError:
        update.message.reply_text("Missing argument!")


def geoip(update: Update, context: CallbackContext) -> None:
    try:
        reply = ''
        data =[]
        url = 'https://api.shodan.io/dns/resolve?hostnames=' + context.args[0] + '&key=' + os.environ.get("SHODAN_API_KEY")
        response = requests.get(url)
        IP = response.json()[context.args[0]]
        api = shodan.Shodan(os.environ.get("SHODAN_API_KEY"))
        host = api.host(IP)
        data.append('Organization : ' + host["org"])
        data.append('Isp : ' + host["data"][1]["isp"])
        data.append('Asn : ' + host["data"][1]["asn"])
        data.append('Country : ' + host["data"][1]["location"]["country_name"])
        data.append('City : ' + host["data"][1]["location"]["city"])
        data.append('Longitude : ' + str(host["data"][1]["location"]["longitude"]))
        data.append('Latitude : ' + str(host["data"][1]["location"]["latitude"]))
        reply ='\n'.join(data)
        update.message.reply_text(reply)

    except(shodan.APIError,TypeError,KeyError):
        update.message.reply_text("Couldn't resolve the host!")
    except requests.exceptions.ConnectionError as e:
        update.message.reply_text("Couldn't resolve! Connection error!")
    except IndexError:
        update.message.reply_text("Missing argument!")


def zoomscan(update: Update, context: CallbackContext) -> None: 
    try:
        reply = ''
        data =[]
        headers = {
        'API-KEY': os.environ.get("ZOOMEYE_APIKEY"),
        }

        params = (
            ('q', context.args[0]),
        )

        response = requests.get('https://api.zoomeye.org/domain/search', headers=headers, params=params)
        jobjects = json.loads(response.text)
        data.append('COUNT: ' + str(jobjects["total"]))
        for jobj in jobjects["list"]:
            data.append('HOST: ' + jobj["name"])
            data.append('TIMESTAMP: ' + jobj["timestamp"])
        reply ='\n'.join(data)
        update.message.reply_text(reply)
        
    except IndexError:
        update.message.reply_text("Missing argument!")
    except(TypeError,KeyError):
        update.message.reply_text("Couldn't resolve  the host!")
    except requests.exceptions.ConnectionError as e:
        update.message.reply_text("Couldn't resolve! Connection error!")


def help(update, context):
    update.message.reply_text("""Usage:  /command <query> \n
      Available commands:
      /find <Name:Surname> - Search for a person by name&surname.
      /phone - Search for a a person by phonenumber (/find 385123456789)
      /whois - WHOIS lookup.
      /cve - Scan the target for cve details using shodan.
      /domains - Search for associated domain names using zoomeye. 
      /geoip - Lookup target geoip info.
      /bihreg <platenum> - Lookup info on bosnian car license plates.
      /croreg <platenum> - Lookup info on croatian car license plates.
    """)


def main() -> None:
    # Create the updater and pass it your bot's token.
    bot = Updater(os.environ.get("BOT_TOKEN"))
    users = list(map(int, os.environ.get("USERS").split('|')))

    # Get the dispatcher to register handlers.
    dispatcher = bot.dispatcher
    dispatcher.add_handler(CommandHandler("phone", phone, Filters.user(user_id=users)))
    dispatcher.add_handler(CommandHandler("whois", who, Filters.user(user_id=users)))
    dispatcher.add_handler(CommandHandler("cve", cvescan, Filters.user(user_id=users)))
    dispatcher.add_handler(CommandHandler("bihreg", bihreg, Filters.user(user_id=users)))
    dispatcher.add_handler(CommandHandler("croreg", croreg, Filters.user(user_id=users)))
    dispatcher.add_handler(CommandHandler("find", find, Filters.user(user_id=users))) 
    dispatcher.add_handler(CommandHandler("geoip", geoip, Filters.user(user_id=users)))
    dispatcher.add_handler(CommandHandler("domains", zoomscan, Filters.user(user_id=users)))
    dispatcher.add_handler(CommandHandler("help", help, Filters.user(user_id=users)))

    # Sta
    # rt the bot.
    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    main()



