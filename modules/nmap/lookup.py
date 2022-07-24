from telegram import Update
from telegram.ext import CallbackContext
import requests
import json
import os
import modules.message.sendmessage as message


def domains(update: Update, context: CallbackContext) -> None:  # TODO test this function
    try:
        if len(context.args) == 0:
            message.sendmessage("Usage:  /domains example.com",update)
        else:
            response = requests.get(os.environ.get("API_URL") + "nmap/subdomains?domain=%s" %context.args[0])
            jobjects = json.loads(response.text)
            if jobjects.get("status") == "FAILED":
                message.sendmessage("There was an error !")
            else:
                message.sendmessage(jobjects.get("data"),update)
    except IndexError:
        message.sendmessage("Missing argument!",update)
    except(TypeError,KeyError) as e:
        print(e)
    except requests.exceptions.ConnectionError:
        message.sendmessage("Couldn't resolve! Connection error!",update)
    except requests.exceptions.RequestException as e:
        message.sendmessage("Request timed out. Server is not responding.",update)

def nmap_scan(update: Update, context: CallbackContext) -> None: 
    try:
        if len(context.args) == 0:
                message.sendmessage("""Usage:  /nmap target.com t
      *Available scan profiles*:\n
      t - traceroute.
      is - intense scan.
      isudp - intense scan w/udp.
      istcp - intense scan w/tcp.
      ping - ping scan.
      qsp - quickscan plus.""",update)
        else:
            response = requests.get(os.environ.get("API_URL") + "nmap/" + "%s" %setcommand(context.args[1]) + "?target=%s" %context.args[0])
            jobjects = json.loads(response.text)
            message.sendmessage(jobjects.get("data"),update)
    except IndexError:
        message.sendmessage("Missing argument!",update)
    except requests.exceptions.RequestException as e:
        message.sendmessage("Request timed out. Server is not responding.",update)


def setcommand(argument):
    match argument:
        case "t":
            return "traceroute"
        case "is":
            return "intscan"
        case "isudp":
            return "intscanudp"
        case "istcp":
            return "intscantcp"
        case "ping":
            return "ping"
        case "qsp":
            return "quickscan"
        case _:
            return "traceroute"
