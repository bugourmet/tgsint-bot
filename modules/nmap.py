from telegram import Update
from telegram.ext import CallbackContext
import requests
import json
import os
from .message import sendmessage


def domains(update: Update, context: CallbackContext) -> None:  # TODO test this function
    try:
        if len(context.args) == 0:
            update.message.reply_text("Usage:  /domains example.com")
        else:
            response = requests.get(os.environ.get("API_URL") + "nmap/subdomains?domain=%s" %context.args[0])
            jobjects = json.loads(response.text)
            if jobjects.get("status") == "FAILED":
                update.message.reply_text("There was an error !")
            else:
                sendmessage(jobjects.get("data"),update)
    except IndexError:
        update.message.reply_text("Missing argument!")
    except(TypeError,KeyError) as e:
        print(e)
    except requests.exceptions.ConnectionError:
        update.message.reply_text("Couldn't resolve! Connection error!")

def nmap_scan(update: Update, context: CallbackContext) -> None: 
    try:
        if len(context.args) == 0:
                update.message.reply_text("""Usage:  /nmap target.com t
      Available scan profiles:\n
      t - traceroute.
      is - intense scan.
      isudp - intense scan w/udp.
      istcp - intense scan w/tcp.
      ping - ping scan.
      qsp - quickscan plus.""")
        else:
            response = requests.get(os.environ.get("API_URL") + "/nmap/" + "%s" %setcommand(context.args[1]) + "?target=%s" %context.args[0])
            jobjects = json.loads(response.text)
            sendmessage(jobjects.get("data"),update)
    except IndexError:
        update.message.reply_text("Missing argument!")
    except requests.exceptions.ConnectionError:
        update.message.reply_text("Couldn't resolve! Connection error!")

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
