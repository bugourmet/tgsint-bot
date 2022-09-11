from telegram import Update
from telegram.ext import CallbackContext
import requests
import json
import os,re
import modules.message.sendmessage as message


def bihreg(update: Update, context: CallbackContext) -> None:
    try:
        if len(context.args) == 0:
            message.sendmessage("Usage:  /bihreg E94-X-XXX ",update)
        else:
            if len(context.args[0]) < 5:
                message.sendmessage("Please enter a query longer than 5 chars.",update)
            else:
                response = requests.get(os.environ.get("API_URL") + "carlookup/bih?plates=%s" %context.args[0])
                jobjects = json.loads(response.text)
                message.sendmessage(jobjects.get("data"),update)

    except requests.exceptions.RequestException as e:
        message.sendmessage("Request timed out. Server is not responding.",update)
    except IndexError:
        message.sendmessage("Missing argument!")


def croreg(update: Update, context: CallbackContext) -> None:
    try:
        if len(context.args) == 0:
            message.sendmessage("Usage:  /croreg ZGXXXXX",update)
        else:
            if len(context.args[0]) < 5:
                message.sendmessage("Please enter a query longer than 5 chars.",update)
            else:
                response = requests.get(os.environ.get("API_URL") + "carlookup/hr?plates=%s" %context.args[0])
                data = []
                reply = ''
                jobjects = json.loads(response.text)
                if jobjects.get("status") == "FAILED":
                    message.sendmessage("Vehicle Details Not Found!",update)
                if len(jobjects.get("data").get("vehiclePolicyDetails"))== 0:
                    message.sendmessage("Vehicle Details Not Found!",update)
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
                    message.sendmessage(reply,update)
                    vin = str(jobjects.get("data").get("vinNumber"))
                    month = str(jobjects.get("data").get("vehiclePolicyDetails").get("policyExpirationDate")).split("-")
                    response = requests.get(os.environ.get("API_URL") + "carlookup/vin?number=%s"%vin + "&month=%s" %month[1] )
                    jobjects = json.loads(response.text)
                    exam_result = re.sub(re.compile('<.*?>') , '', str(jobjects.get("data").get("response"))).replace("Preuzmi u Excel formatu","")
                    message.sendmessage(exam_result,update)
    except requests.exceptions.RequestException as e:
        message.sendmessage("Request timed out. Server is not responding.",update)
    except KeyError as e:
        print(e)
    except IndexError:
        message.sendmessage("Missing argument!",update)