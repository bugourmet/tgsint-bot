import os
import json
import telegram
from telegram import Update
from telegram.ext import CallbackContext
import requests
import modules.message.sendmessage as message


def find(update: Update, context: CallbackContext) -> None:
    """Function used for finding people by phone number"""
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
                    result = [str(jobj.get("fbid")),
                              str(jobj.get("name")),
                              str(jobj.get("surname")),
                              str(jobj.get("sex")),
                              str(jobj.get("location")),
                              str(jobj.get("extra"))]
                    data.append('\nPhone Number: +' +
                                str(jobj.get("phonenum")))
                    data.append(
                        f'FB link:  https://www.facebook.com/{result[0]}')
                    data.append(f'Name: {result[1]}')
                    data.append(f'Surname: {result[2]}')
                    data.append(f'Sex: {result[3]}')
                    data.append(f'Location: {result[4]}')
                    data.append(f'Extra Info: {result[5]}')
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
    """Function used for finding people by phone number"""
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


def phonebook(update: Update, context: CallbackContext) -> None:
    """Function used for finding people on phonebooks"""
    try:
        if len(context.args) == 0:
            message.sendmessage(
                "Usage:  /pb <name> <surname>  optional: <location>", update)
        else:
            data = []
            reply = ''
        if len(context.args[0]) < 3 or len(context.args[1]) < 3:
            message.sendmessage(
                "Name must be longer than 3 chars.", update)
        else:
            if len(context.args) > 2:
                location = context.args[2]
            else:
                location = ""
            response = requests.get(os.environ.get(
                "API_URL") + f"phonebook/find?name={context.args[0]}&surname={context.args[1]}&location={location}", timeout=5)
            res_obj = json.loads(response.text)
            if len(res_obj.get("result")) == 0:
                reply = "User not found!"
            else:
                for jobj in res_obj.get("result"):
                    result = [str(jobj.get("name")),
                              str(jobj.get("address")),
                              str(jobj.get("number"))]
                    data.append(f"Name: {result[0]}")
                    data.append(f"Address: {result[1]}")
                    data.append(f"Number: {result[2]}\n")
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
