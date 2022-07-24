import telegram
from telegram import Update
from telegram.ext import CallbackContext
import requests
import json
import os
import modules.message.sendmessage as message


def find(update: Update, context: CallbackContext) -> None:
    try:
        if len(context.args) == 0:
            message.sendmessage("Usage:  /find Name Surname ",update)
        else:
            data = []
            reply = ''
            response = requests.get(os.environ.get("API_URL") + "person/find?name=%s" %context.args[0] + "&surname=%s" %context.args[1])
            jobjects = json.loads(response.text)
            if jobjects.get("status") == "FAILED" or jobjects.get("error"):
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
            message.sendmessage(reply,update)
    except requests.exceptions.RequestException as e:
        message.sendmessage("Request timed out. Server is not responding.",update)
    except KeyError as e:
        print("KeyError",e)
    except IndexError:
        message.sendmessage("Missing argument!",update)
    except telegram.error.BadRequest as e:
        print(e)


def phone(update: Update, context: CallbackContext) -> None:        
    try:
        if len(context.args) == 0:
            message.sendmessage("Usage:  /phone 385123456789",update)
        else:
            if "+" in context.args[0]:
                context.args[0]=(context.args[0]).replace("+","")
            response = requests.get(os.environ.get("API_URL") + "person/phone?number=%s" %context.args[0])
            data = []
            reply = ''
            jobjects = json.loads(response.text)
            if jobjects.get("status") == "FAILED" or jobjects.get("error"):
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
            message.sendmessage(reply,update)

    except requests.exceptions.RequestException as e:
        message.sendmessage("Request timed out. Server is not responding.",update)
    except KeyError as e:
        print("KeyError",e)
    except IndexError:
        message.sendmessage("Missing argument!",update)
        

def whois(update: Update, context: CallbackContext) -> None:
    try:
        if len(context.args) == 0:
            message.sendmessage("Usage:  /whois example.com",update)
        else:
            data = []
            reply = ''
            response = requests.get(os.environ.get("API_URL") + "whois?domain=%s" %context.args[0])
            jobjects = json.loads(response.text)
            resData = jobjects.get("data")
            for server in resData:
                for info in resData[server]:
                    data.append(info + str(resData[server].get(info)) )
                reply = '\n'.join(data)
            message.sendmessage(reply,update)

    except requests.exceptions.RequestException as e:
        message.sendmessage("Request timed out. Server is not responding.",update)
    except KeyError as e:
        print("KeyError",e)
    except IndexError:
        message.sendmessage("Missing argument!",update)