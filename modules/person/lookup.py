import os
import logging
from telegram import Update
from telegram.ext import CallbackContext
import modules.message.sendmessage as message
import pymongo

mongo_url = os.environ.get('MONGODB_URL')
database_name = os.environ.get("DB_NAME")
collection_name = os.environ.get("COLLECTION_NAME")
client = pymongo.MongoClient(mongo_url)
database = client[database_name]
collection = database[collection_name]

def find(update: Update, context: CallbackContext) -> None:
    """Function used for finding people by name and surname"""
    try:
        if len(context.args) < 2:
            message.sendmessage("Usage: /find Name Surname", update)
            return

        query = {
            "name": {"$regex": context.args[0], "$options": "i"},
            "surname": {"$regex": context.args[1], "$options": "i"}
        }
        results = list(collection.find(query))

        if not results:
            message.sendmessage("User not found", update)
            return

        data = []
        for result in results:
            data.append(f"\n*Phone Number: * {result.get('phonenum')}")
            data.append(f"*Facebook ID: * {result.get('fbid')}")
            data.append(f"*Name: * {result.get('name')} {result.get('surname')}")
            data.append(f"*Sex: * {result.get('sex')}")
            data.append(f"*Location: * {result.get('location')}")
            data.append(f"*Extra: * {result.get('extra')}")

        reply = '\n'.join(data)
        message.sendmessage(reply, update)

    except KeyError as err:
        logging.error("KeyError: %s", err)
        message.sendmessage("An error occurred while processing your request.", update)
    except IndexError:
        message.sendmessage("Missing argument!", update)


def phone(update: Update, context: CallbackContext) -> None:
    """Function used for finding people by phone number"""
    try:
        if len(context.args) == 0:
            message.sendmessage("Usage: /phone 385123456789", update)
            return

        phone_number = context.args[0].replace("+", "")

        query = {"phonenum": phone_number}
        results = list(collection.find(query))

        if not results:
            message.sendmessage("User not found", update)
            return

        data = []
        for result in results:
            data.append(f"\n*Phone Number: * {result.get('phonenum')}")
            data.append(f"*Facebook ID: * {result.get('fbid')}")
            data.append(f"*Name: * {result.get('name')} {result.get('surname')}")
            data.append(f"*Sex: * {result.get('sex')}")
            data.append(f"*Location: * {result.get('location')}")
            data.append(f"*Extra: * {result.get('extra')}")

        reply = '\n'.join(data)
        message.sendmessage(reply, update)

    except KeyError as err:
        logging.error("KeyError: %s", err)
        message.sendmessage("An error occurred while processing your request.", update)
    except IndexError:
        message.sendmessage("Missing argument!", update)