import os
import logging
from telegram import Update
from telegram.ext import CallbackContext
import modules.message.sendmessage as message
import pymongo

api_url = os.environ.get('API_URL')
mongo_url = os.environ.get('MONGODB_URL')
client = pymongo.MongoClient(mongo_url)
database = client["database"]
collection = database["persons"]

def find(update: Update,context: CallbackContext) -> None:
    """Function used for finding people by phone number"""
    try:
        if len(context.args) == 0:
            message.sendmessage("Usage:  /find Name Surname ", update)
        else:
            query = {
                "name": {"$regex": f"{context.args[0]}", "$options": "i"},
                "surname": {"$regex": f"{context.args[1]}", "$options": "i"}
            }
            results = list(collection.find(query))
            for result in results:
                formatted_message = (
                f"*ID: * {result.get('_id')}\n"
                f"*Phone Number: * {result.get('phonenum')}\n"
                f"*Facebook ID: * {result.get('fbid')}\n"
                f"*Name: * {result.get('name')} {result.get('surname')}\n"
                f"*Sex: * {result.get('sex')}\n"
                f"*Location: * {result.get('location')}\n"
                f"*Extra: * {result.get('extra')}\n"
            )
                message.sendmessage(formatted_message,update)
    except KeyError as err:
        logging.error("KeyError: %s", err)
    except IndexError:
        message.sendmessage("Missing argument!", update)

def phone(update: Update, context: CallbackContext) -> None:
    """Function used for finding people by phone number"""
    try:
        if len(context.args) == 0:
            message.sendmessage("Usage:  /phone 385123456789", update)
        else:
            if "+" in context.args[0]:
                context.args[0] = (context.args[0]).replace("+", "")
            query = {"phonenum": context.args[0]}
            results = list(collection.find(query))
            for result in results:
                formatted_message = (
                f"*ID: * {result.get('_id')}\n"
                f"*Phone Number: * {result.get('phonenum')}\n"
                f"*Facebook ID: * {result.get('fbid')}\n"
                f"*Name: * {result.get('name')} {result.get('surname')}\n"
                f"*Sex: * {result.get('sex')}\n"
                f"*Location: * {result.get('location')}\n"
                f"*Extra: * {result.get('extra')}\n"
            )
                message.sendmessage(formatted_message,update)
    except KeyError as err:
        logging.error("KeyError: %s", err)
    except IndexError:
        message.sendmessage("Missing argument!", update)
