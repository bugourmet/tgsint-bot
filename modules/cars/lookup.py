import os
import json
import re
from telegram import Update
from telegram.ext import CallbackContext
import requests
import modules.message.sendmessage as message


def croreg(update: Update, context: CallbackContext) -> None:
    """Function used for fetching croatian plates info and vehicle inspection data"""
    try:
        if len(context.args) == 0:
            message.sendmessage("Usage:  /croreg ZGXXXXX", update)
        else:
            if len(context.args[0]) < 5:
                message.sendmessage(
                    "Please enter a query longer than 5 chars.", update)
            else:
                response = requests.get(os.environ.get(
                    "API_URL") + f"carlookup/hr?plates={context.args[0]}", timeout=5)
                data = []
                reply = ''
                res_obj = json.loads(response.text)
                result = res_obj.get("result")
                if len(result) == 0 or result.get("status") == 404:
                    message.sendmessage("Vehicle Details Not Found!", update)
                else:
                    result = res_obj.get("result")
                    results = [result.get("policyExpirationDate"),
                               result.get("policyNumber"),
                               result.get("vin"),
                               result.get("type"),
                               result.get("manufacturer"),
                               result.get("model"),
                               result.get("line"),
                               result.get("fuelType"),
                               str(result.get("year")),
                               result.get("color"),
                               str(result.get("kw"))]
                    data.append(f"Istek Police: {results[0]}")
                    data.append(f"Broj Police: {results[1]}")
                    data.append(f"VIN: {results[2]}")
                    data.append(f"Tip Automobila: {results[3]}")
                    data.append(f"Marka: {results[4]}")
                    data.append(f"Model: {results[5]}")
                    data.append(f"Linija: {results[6]}")
                    data.append(f"Tip Goriva: {results[7]}")
                    data.append(f"Godina Proizvodnje: {results[8]}")
                    data.append(f"Boja: {results[9]}")
                    data.append(f"Snaga(kW): {results[10]}")
                    reply = '\n'.join(data)
                    message.sendmessage(reply, update)
                    month = str(results[0]).split("-")
                    response = requests.get(os.environ.get(
                        "API_URL") + f"carlookup/vin?number={results[2]}&month={month[1]}", timeout=5)
                    res_obj = json.loads(response.text)
                    exam_result = re.sub(re.compile(
                        '<.*?>'), '', str(res_obj.get("response"))).replace("Preuzmi u Excel formatu", "")
                    message.sendmessage(exam_result, update)
    except requests.exceptions.RequestException:
        message.sendmessage(
            "Request timed out. Server is not responding.", update)
    except KeyError as err:
        print(err)
    except IndexError:
        message.sendmessage("Missing argument!", update)
    except TypeError:
        message.sendmessage("TypeError!", update)
