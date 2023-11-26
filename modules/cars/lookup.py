from telegram import Update
from telegram.ext import CallbackContext
import requests
import modules.message.sendmessage as message
import logging

# def checkvin(vin, month,update: Update):
#     """Function used for fetching vehicle inspection data"""
#     try:
#         url = "https://www.cvh.hr/Umbraco/Surface/TabsSurface/mot"
#         data = {"VIN": vin, "month": month}
#         headers = {
#             "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
#         }
#         encoded_data = urlencode(data)

#         response = requests.post(url, data=encoded_data, headers=headers, verify=False,timeout=5)
#         if response.ok:
#             data = response.json()
#             return data
#         else:
#             response.raise_for_status()
#     except requests.exceptions.RequestException:
#         message.sendmessage(
#             "Request timed out. Server is not responding.", update)
#         return None

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
                api_url = f"https://api.laqo.hr/webshop/backend/vehicle-api/v2/vehicles?plateNumber={context.args[0]}"
                response = requests.get(api_url,timeout=5)

                if response.ok:
                    data = response.json()
                    formatted_message = (
                    f"*Istek Police: * {data.get('policyExpirationDate')}\n"
                    f"*Broj Police: * {data.get('policyNumber')}\n"
                    f"*VIN: * {data.get('vin')}\n"
                    f"*Tip Automobila: * {data.get('type')}\n"
                    f"*Marka: * {data.get('manufacturer')}\n"
                    f"*Model: * {data.get('model')}\n"
                    f"*Linija: * {data.get('line')}\n"
                    f"*Tip Goriva: * {data.get('fuelType')}\n"
                    f"*Godina Proizvodnje: * {data.get('year')}\n"
                    f"*Boja: * {data.get('color')}\n"
                    f"*Snaga(kW): * {data.get('kw')}\n"
                    )
                    message.sendmessage(formatted_message, update)

                else:
                    message.sendmessage(
                    "Failed to retrieve data from the API.", update)
    except requests.exceptions.RequestException:
        message.sendmessage(
            "Request timed out. Server is not responding.", update)
    except KeyError as err:
        logging.error(err)
    except IndexError:
        message.sendmessage("Missing argument!", update)
    except TypeError:
        message.sendmessage("TypeError!", update)
