import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler,Filters, CallbackContext
import logging
import requests
import json
import shodan
from bs4 import BeautifulSoup
import os,re,datetime
from dotenv import load_dotenv

#logging.basicConfig(filename='log.txt', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv() 


def error(update, context): 
    logger.warning("%s" ' caused error: "%s"', update, context.error)


def splitmessage(message):
    message_list = []
    if len(message) > 4096:
        for x in range(0, len(message), 4096):
            message_list.append(message[x:x+4096])
    else:
        message_list.append(message)
    return message_list


def sendmessage(reply,update):
    messages = splitmessage(reply)
    for message in messages:
        update.message.reply_text(message)


def find(update: Update, context: CallbackContext) -> None:
    try:
        if len(context.args) == 0:
            update.message.reply_text("Usage:  /find Name Surname ")
        else:
            response = requests.get(os.environ.get("API_URL") + "find?name=%s"%context.args[0] + "&surname=%s"%context.args[1])
            data = []
            reply = ''
            jobjects = json.loads(response.text)
            for jobj in jobjects:
                if jobj == "error":
                    reply = "User not found!"
                else:
                    data.append('Phone Number: +'                       + str(jobj.get("phonenum")))
                    data.append('FB link:  https://www.facebook.com/'   + str(jobj.get("fbid")))
                    data.append('Name: '                                + str(jobj.get("name")))
                    data.append('Surname: '                             + str(jobj.get("surname")))
                    data.append('Sex: '                                 + str(jobj.get("sex")))
                    data.append('Extra Info: '                          + str(jobj.get("extra")))
                    reply = '\n'.join(data) 
            sendmessage(reply,update)
    except requests.exceptions.RequestException as e:
        print(e)
    except KeyError as e:
        print(e)
    except IndexError:
        update.message.reply_text("Missing argument!")
    except telegram.error.BadRequest as e:
        print(e)


def phone(update: Update, context: CallbackContext) -> None:        
    try:
        if len(context.args) == 0:
            update.message.reply_text("Usage:  /phone 385123456789")
        else:
            if "+" in context.args[0]:
                context.args[0]=(context.args[0]).replace("+","")
            response = requests.get(os.environ.get("API_URL") + "phone?number=%s"%context.args[0])
            data = []
            reply = ''
            jobjects = json.loads(response.text)
            for jobj in jobjects:
                if jobj == "error":
                    reply = "User not found!"
                else:
                    data.append('Phone Number: +'                       + str(jobj.get("phonenum")))
                    data.append('FB link:  https://www.facebook.com/'   + str(jobj.get("fbid")))
                    data.append('Name: '                                + str(jobj.get("name")))
                    data.append('Surname: '                             + str(jobj.get("surname")))
                    data.append('Sex: '                                 + str(jobj.get("sex")))
                    data.append('Extra Info: '                          + str(jobj.get("extra")))
                    reply = '\n'.join(data) 
            sendmessage(reply,update)

    except requests.exceptions.RequestException as e:
        print(e)
    except KeyError as e:
        print(e)
    except IndexError:
        update.message.reply_text("Missing argument!")


def whois(update: Update, context: CallbackContext) -> None:
    try:
        if len(context.args) == 0:
            update.message.reply_text("Usage:  /whois example.com")
        else:
            data = []
            reply = ''
            response = requests.get(os.environ.get("API_URL") + "whois?domain=%s"%context.args[0])
            jobjects = json.loads(response.text)
            for server in jobjects:
                for info in(jobjects[server]):
                    data.append("%s : " %info  + str(jobjects[server][info]))
                reply = '\n'.join(data)
            sendmessage(reply,update)

    except requests.exceptions.RequestException as e:
        print(e)
    except KeyError as e:
        print(e)
    except IndexError:
        update.message.reply_text("Missing argument!")


def cvescan(update: Update, context: CallbackContext) -> None:
    try:
        if len(context.args) == 0:
            update.message.reply_text("Usage:  /cve example.com ")
        else:
            reply = ''
            vulns = []
            ports = []
            url = 'https://api.shodan.io/dns/resolve?hostnames=%s'%context.args[0] + '&key=%s'%os.environ.get("SHODAN_API_KEY")
            response = requests.get(url)
            IP = response.json()[context.args[0]]
            api = shodan.Shodan(os.environ.get("SHODAN_API_KEY"))
            host = api.host(IP)

            if host.get('vulns') != None:
                for item in host.get('data'):
                    ports.append(item.get('port'))
            else:
                ports.append(None)

            if host.get('vulns') != None:
                for item in host.get('vulns'):
                    vulns.append(item)
                    reply = '\n'.join(vulns)
            else:
                reply = ("NO CVE DATA!")
            sendmessage(("TARGET IP: %s" %str(IP) + "\n\nCVE: \n\n%s" %reply + "\n\nPORTS: %s" %str(ports)),update)

    except requests.exceptions.ConnectionError:
        update.message.reply_text("Couldn't resolve! Connection error!")
    except(shodan.APIError) as e:
        update.message.reply_text(str(e))
    except IndexError:
        update.message.reply_text("Missing argument!")


def bihreg(update: Update, context: CallbackContext) -> None:
    try:
        if len(context.args) == 0:
            update.message.reply_text("Usage:  /bihreg E94-X-XXX ")
        else:
            if len(context.args[0]) < 5:
                update.message.reply_text("Please enter a query longer than 5 chars.")
            else:
                date=datetime.date.today()
                searchdate =(date.strftime('%d.%m.%Y'))

                params = (
                    ('kat', '82'),
                )

                data = {
                'searchRegNr': context.args[0],
                'searchDate': searchdate,
                'third_email': '',
                'action': 'doSearch',
                'mode': 'print',
                'btnSearch': 'TRAZI'
                }

                response = requests.post('https://www.bzkbih.ba/ba/stream.php', params=params, data=data)
                soup = BeautifulSoup(response.content, 'lxml')
                result = soup.find("td", {"colspan": "2"})
                if "vozilo se ne može pronaći" in result.text:
                    update.message.reply_text("Vehicle Details Not Found!")
                else:
                    sendmessage(result.text,update)

    except requests.exceptions.RequestException as e:
        print(e)
    except IndexError:
        update.message.reply_text("Missing argument!")


def croreg(update: Update, context: CallbackContext) -> None:
    try:
        if len(context.args) == 0:
            update.message.reply_text("Usage:  /croreg ZGXXXXX")
        else:
            if len(context.args[0]) < 5:
                update.message.reply_text("Please enter a query longer than 5 chars.")
            else:
                response = requests.post('https://api.laqo.hr/webshop/ace/api/v1/car/details',json={'plateNumber':(context.args[0]).upper()})
                data = []
                reply = ''
                jobjects = json.loads(response.text)
                if "statusCode" in jobjects:
                    update.message.reply_text("Vehicle Details Not Found!")
                else:
                    data.append('Istek Police: '        + str(jobjects.get("vehiclePolicyDetails").get("policyExpirationDate")))
                    data.append('Broj Police: '         + str(jobjects.get("vehiclePolicyDetails").get("policyNumber")))
                    data.append('VIN: '                 + str(jobjects.get("vinNumber")))
                    data.append('Tip Automobila: '      + str(jobjects.get("vehicleType")))  
                    data.append('Marka: '               + str(jobjects.get("vehicleManufacturerName")))
                    data.append('Model: '               + str(jobjects.get("model")))
                    data.append('Linija: '              + str(jobjects.get("line")))
                    data.append('Tip Goriva: '          + str(jobjects.get("fuelType")))
                    data.append('Godina Proizvodnje: '  + str(jobjects.get("yearOfManufacture")))
                    data.append('Boja: '                + str(jobjects.get("color")))
                    data.append('Snaga(kW): '           + str(jobjects.get("kw")))
                    reply = '\n'.join(data)
                    sendmessage(reply,update)

                    month = str(jobjects.get("vehiclePolicyDetails").get("policyExpirationDate")).split("-")
                    data = {    
                    'VIN': str(jobjects["vinNumber"]),
                    'month': month[1]
                    }

                    response = requests.post('https://www.cvh.hr/Umbraco/Surface/TabsSurface/mot',data=data)
                    jobjects = json.loads(response.text)
                    exam_result = re.sub(re.compile('<.*?>') , '', str(jobjects.get("response"))).replace("Preuzmi u Excel formatu","")
                    sendmessage(exam_result,update)

    except requests.exceptions.RequestException as e:
        print(e)
    except KeyError as e:
        print(e)
    except IndexError:
        update.message.reply_text("Missing argument!")


def geoip(update: Update, context: CallbackContext) -> None:
    try:
        if len(context.args) == 0:
            update.message.reply_text("Usage:  /geoip 8.8.8.8")
        else:
            reply = ''
            data = []
            url = 'https://api.shodan.io/dns/resolve?hostnames=%s'%context.args[0] + '&key=%s'%os.environ.get("SHODAN_API_KEY")
            response = requests.get(url)
            IP = response.json()[context.args[0]]
            api = shodan.Shodan(os.environ.get("SHODAN_API_KEY"))
            host = api.host(IP)
            data.append('Organization : ' + str(host.get("org")))
            data.append('Isp : '          + str(host.get("data")[1].get("isp")))
            data.append('Asn : '          + str(host.get("data")[1]["asn"]))
            data.append('Country : '      + str(host.get("data")[1].get("location").get("country_name")))
            data.append('City : '         + str(host.get("data")[1].get("location").get("city")))
            data.append('Longitude : '    + str(host.get("data")[1].get("location").get("longitude")))
            data.append('Latitude : '     + str(host.get("data")[1].get("location").get("latitude")))
            reply ='\n'.join(data)
            sendmessage(reply,update)

    except(shodan.APIError,TypeError,KeyError):
        update.message.reply_text("Couldn't resolve the host!")
    except requests.exceptions.ConnectionError:
        update.message.reply_text("Couldn't resolve! Connection error!")
    except IndexError:
        update.message.reply_text("Missing argument!")


def domains(update: Update, context: CallbackContext) -> None: 
    try:
        if len(context.args) == 0:
            update.message.reply_text("Usage:  /domains example.com")
        else:
            response = requests.get(os.environ.get("API_URL") + "nmap?target=%s"%context.args[0] + "&option=9")
            jobjects = json.loads(response.text)
            if jobjects.get("result") == "":
                sendmessage("Couldn't resolve! Check the domain!",update)
            else: 
                sendmessage(jobjects.get("result"),update)
    except IndexError:
        update.message.reply_text("Missing argument!")
    except(TypeError,KeyError):
        update.message.reply_text("Couldn't resolve the host!")
    except requests.exceptions.ConnectionError:
        update.message.reply_text("Couldn't resolve! Connection error!")


def nmap_scan(update: Update, context: CallbackContext) -> None: 
    try:
        if len(context.args) == 0:
                update.message.reply_text("""Usage:  /nmap target.com qt
      Available scan profiles:\n
      qt - quick traceroute.
      is - intense scan.
      isudp - intense scan w/udp.
      istcp - intense scan w/tcp.
      isnp - intense scan,no ping.
      ping - ping scan.
      qs - quickscan.
      qsp - quickscan plus.""")
        else:
            response = requests.get(os.environ.get("API_URL") + "nmap?target=%s"%context.args[0] + "&option=%s"%setcommand(context.args[1]))
            jobjects = json.loads(response.text)
            sendmessage(jobjects.get("result"),update)
    except IndexError:
        update.message.reply_text("Missing argument!")
    except requests.exceptions.ConnectionError:
        update.message.reply_text("Couldn't resolve! Connection error!")

def setcommand(agrument):
    match agrument:
        case "qt":
            return "1"
        case "is":
            return "2"
        case "isudp":
            return "3"
        case "istcp":
            return "4"
        case "isnp":
            return "5"
        case "ping":
            return "6"
        case "qs":
            return "7"
        case "qsp":
            return "8"

def help(update, context):
    update.message.reply_text("""Usage:  /command <query> 
      Available commands:\n
      /find - Person lookup.
      /phone - Phone number lookup.
      /whois - WHOIS lookup.
      /cve - Scan the target for cve details using shodan.
      /domains - Search for associated domain names. 
      /geoip - Lookup target geoip info.
      /bihreg - Lookup bosnian car license plates.
      /croreg - Lookup croatian car license plates.
      /nmap - Nmap scan w/custom nmap commands.
    """)


def main() -> None:
    # Create the updater and pass it your bot's token.
    bot = Updater(os.environ.get("BOT_TOKEN"))
    users = list(map(int, os.environ.get("USERS").split('|')))

    # Get the dispatcher to register handlers.
    dispatcher = bot.dispatcher
    dispatcher.add_error_handler(error)
    dispatcher.add_handler(CommandHandler("phone", phone, Filters.user(user_id=users)))
    dispatcher.add_handler(CommandHandler("whois", whois, Filters.user(user_id=users)))
    dispatcher.add_handler(CommandHandler("cve", cvescan, Filters.user(user_id=users)))
    dispatcher.add_handler(CommandHandler("bihreg", bihreg, Filters.user(user_id=users)))
    dispatcher.add_handler(CommandHandler("croreg", croreg, Filters.user(user_id=users)))
    dispatcher.add_handler(CommandHandler("find", find, Filters.user(user_id=users)))
    dispatcher.add_handler(CommandHandler("geoip", geoip, Filters.user(user_id=users)))
    dispatcher.add_handler(CommandHandler("domains", domains, Filters.user(user_id=users)))
    dispatcher.add_handler(CommandHandler("nmap", nmap_scan, Filters.user(user_id=users)))
    dispatcher.add_handler(CommandHandler("help", help, Filters.user(user_id=users)))

    # Start the bot.
    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    main()