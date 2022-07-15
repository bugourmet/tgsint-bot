import telegram
from telegram import Update
from telegram.ext import CallbackContext
import requests
import json
import os,re
from .message import sendmessage


def find(update: Update, context: CallbackContext) -> None:
    try:
        if len(context.args) == 0:
            update.message.reply_text("Usage:  /find Name Surname ")
        else:
            data = []
            reply = ''
            response = requests.get(os.environ.get("API_URL") + "person/find?name=%s " %context.args[0] + "&surname=%s" %context.args[1])
            jobjects = json.loads(response.text)
            if jobjects.get("status") == "FAILED":
                reply = "User not found!"
            else:
                for jobj in jobjects.get("data"):
                    data.append('\nPhone Number: +'                     + str(jobj.get("phonenum")))
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
            response = requests.get(os.environ.get("API_URL") + "person/phone?number=%s" %context.args[0])
            data = []
            reply = ''
            jobjects = json.loads(response.text)
            if jobjects.get("status") == "FAILED":
                reply = "User not found!"
            else:
                for jobj in jobjects.get("data"):
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


def bihreg(update: Update, context: CallbackContext) -> None:
    try:
        if len(context.args) == 0:
            update.message.reply_text("Usage:  /bihreg E94-X-XXX ")
        else:
            if len(context.args[0]) < 5:
                update.message.reply_text("Please enter a query longer than 5 chars.")
            else:
                response = requests.get(os.environ.get("API_URL") + "carlookup/bih?plates=%s" %context.args[0])
                jobjects = json.loads(response.text)
                sendmessage(jobjects.get("data"),update)

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
                response = requests.get(os.environ.get("API_URL") + "carlookup/hr?plates=%s" %context.args[0])
                data = []
                reply = ''
                jobjects = json.loads(response.text)
                if jobjects.get("status") == "FAILED":
                    update.message.reply_text("Vehicle Details Not Found!")
                else:
                    data.append('Istek Police: '        + str(jobjects.get("data").get("vehiclePolicyDetails").get("policyExpirationDate")))
                    data.append('Broj Police: '         + str(jobjects.get("data").get("vehiclePolicyDetails").get("policyNumber")))
                    data.append('VIN: '                 + str(jobjects.get("data").get("vinNumber")))
                    data.append('Tip Automobila: '      + str(jobjects.get("data").get("vehicleType")))  
                    data.append('Marka: '               + str(jobjects.get("data").get("vehicleManufacturerName")))
                    data.append('Model: '               + str(jobjects.get("data").get("model")))
                    data.append('Linija: '              + str(jobjects.get("data").get("line")))
                    data.append('Tip Goriva: '          + str(jobjects.get("data").get("fuelType")))
                    data.append('Godina Proizvodnje: '  + str(jobjects.get("data").get("yearOfManufacture")))
                    data.append('Boja: '                + str(jobjects.get("data").get("color")))
                    data.append('Snaga(kW): '           + str(jobjects.get("data").get("kw")))
                    reply = '\n'.join(data)
                    sendmessage(reply,update)
                    vin = str(jobjects.get("data").get("vinNumber"))
                    month = str(jobjects.get("data").get("vehiclePolicyDetails").get("policyExpirationDate")).split("-")
                    response = requests.get(os.environ.get("API_URL") + "carlookup/vin?number=%s"%vin + "&month=%s" %month[1] )
                    jobjects = json.loads(response.text)
                    exam_result = re.sub(re.compile('<.*?>') , '', str(jobjects.get("data").get("response"))).replace("Preuzmi u Excel formatu","")
                    sendmessage(exam_result,update)
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
            response = requests.get(os.environ.get("API_URL") + "whois?domain=%s" %context.args[0])
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