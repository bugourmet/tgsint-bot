import os
import json
import telegram
from telegram import Update
from telegram.ext import CallbackContext
import requests
import modules.message.sendmessage as message


def find(update: Update, context: CallbackContext) -> None:
    """Function used for finding users by phone number"""
    try:
        if len(context.args) == 0:
            message.sendmessage("Usage:  /find Name Surname ", update)
        else:
            data = []
            reply = ''
            response = requests.get(os.environ.get(
                "API_URL") + f"person/find?name={context.args[0]}&surname={context.args[1]}", timeout=5)
            res_obj = json.loads(response.text)
            if len(res_obj.get("result")) == 0:
                reply = "User not found!"
            else:
                for jobj in res_obj.get("result"):
                    data.append('\nPhone Number: +' +
                                str(jobj.get("phonenum")))
                    data.append(
                        'FB link:  https://www.facebook.com/' + str(jobj.get("fbid")))
                    data.append('Name: ' + str(jobj.get("name")))
                    data.append('Surname: ' + str(jobj.get("surname")))
                    data.append('Sex: ' + str(jobj.get("sex")))
                    data.append('Extra Info: ' + str(jobj.get("extra")))
                    reply = '\n'.join(data)
            message.sendmessage(reply, update)
    except requests.exceptions.RequestException:
        message.sendmessage(
            "Request timed out. Server is not responding.", update)
    except KeyError as err:
        print("KeyError", err)
    except IndexError:
        message.sendmessage("Missing argument!", update)
    except telegram.error.BadRequest as err:
        print(err)


def phone(update: Update, context: CallbackContext) -> None:
    """Function used for finding users by phone number"""
    try:
        if len(context.args) == 0:
            message.sendmessage("Usage:  /phone 385123456789", update)
        else:
            if "+" in context.args[0]:
                context.args[0] = (context.args[0]).replace("+", "")
            response = requests.get(os.environ.get(
                "API_URL") + f"person/phone?number={context.args[0]}", timeout=5)
            data = []
            reply = ''
            res_obj = json.loads(response.text)
            if len(res_obj.get("result")) == 0:
                reply = "User not found!"
            else:
                for jobj in res_obj.get("result"):
                    result = [str(jobj.get("fbid")),
                              str(jobj.get("phonenum")),
                              str(jobj.get("name")),
                              str(jobj.get("surname")),
                              str(jobj.get("sex")),
                              str(jobj.get("extra"))]
                    data.append(f"Phone Number: {result[1]}")
                    data.append(f"FB: https://www.facebook.com/{result[0]}")
                    data.append(f"Name: {result[2]}")
                    data.append(f"Surname: {result[3]}")
                    data.append(f"Sex: {result[4]}")
                    data.append(f"Extra Info: {result[5]}")
                    reply = '\n'.join(data)
            message.sendmessage(reply, update)

    except requests.exceptions.RequestException:
        message.sendmessage(
            "Request timed out. Server is not responding.", update)
    except KeyError as err:
        print(f"KeyError : {err}")
    except IndexError:
        message.sendmessage("Missing argument!", update)
