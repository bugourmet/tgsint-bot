from telegram import Update
from telegram.ext import CallbackContext
import requests
import os
import shodan
from .message import sendmessage

def cvescan(update: Update, context: CallbackContext) -> None:
    try:
        if len(context.args) == 0:
            update.message.reply_text("Usage:  /cve example.com ")
        else:
            reply = ''
            vulns = []
            ports = []
            url = 'https://api.shodan.io/dns/resolve?hostnames=%s' %context.args[0] + '&key=%s'%os.environ.get("SHODAN_API_KEY")
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


def geoip(update: Update, context: CallbackContext) -> None:
    try:
        if len(context.args) == 0:
            update.message.reply_text("Usage:  /geoip 8.8.8.8")
        else:
            reply = ''
            data = []
            url = 'https://api.shodan.io/dns/resolve?hostnames=%s' %context.args[0] + '&key=%s'%os.environ.get("SHODAN_API_KEY")
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
