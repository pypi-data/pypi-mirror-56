#!/usr/bin/env python

from urllib.request import urlopen
import json
import logging
import requests
import socket
import urllib
import urllib3
import os
import time

def get_jsonparsed_data(url):
    """
    Receive the content of ``url``, parse it as JSON and return the object.
    Parameters
    ----------
    url : str
    Returns
    -------
    dict
    """
    data = ""
    try:
        response = urlopen(url)
        data = response.read().decode("utf-8")
        data = json.loads(data)
    except socket.gaierror as err:
        try:
            logging.warning("[Freyr/FinancialModelingPrep.py - get_jsonparsed_data]: " + str(err))
        except urllib.error.URLError as err:
            logging.warning("[Freyr/FinancialModelingPrep.py - get_jsonparsed_data]: " + str(err))
        except urllib3.exceptions.NewConnectionError as err:
            logging.warning("[Freyr/FinancialModelingPrep.py - get_jsonparsed_data]: " + str(err))
        except urllib3.exceptions.MaxRetryError as err:
            logging.warning("[Freyr/FinancialModelingPrep.py - get_jsonparsed_data]: " + str(err))
        except requests.exceptions.ConnectionError as err:
            logging.warning("[Freyr/FinancialModelingPrep.py - get_jsonparsed_data]: " + str(err))
        except UnboundLocalError as err:
            logging.warning("[Freyr/FinancialModelingPrep.py - get_jsonparsed_data]: " + str(err) + ".  Sleeping...")
            time.sleep(3)
            logging.warning("Done")


    return data


def company_profile(symbol):
    symbol = symbol.replace("-", ".")
    url = ("https://financialmodelingprep.com/api/company/profile/" + str(symbol) + "?datatype=json")
    data = []

    try:
        data = get_jsonparsed_data(url)
        data = data[symbol]
    except ValueError as err:
        logging.warning("[Freyr/FinancialModelingPrep.py - company_profile] " + str(symbol) + "$: " + str(err))
    except KeyError as err:
        try:
            logging.warning("[Freyr/FinancialModelingPrep.py - company_profile] " + str(symbol) + "$: " + str(err))
        except NameError:
            logging.warning("[Freyr/FinancialModelingPrep.py - company_profile] Name Error")

    return data

def company_balance_sheet(symbol, rows = 1):
    
    symbol = symbol.replace("-", ".")
    url = "https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/" + str(symbol) + "?period=quarter"
    buffer = []
    count = 0
    try:
        data = get_jsonparsed_data(url)
        data = data['financials']
        for row in data:
            buffer.append(row)

            count += 1
            if count == rows:
                break

        if len(buffer) == 1:
            buffer = buffer[0]
    except TypeError as err:
        logging.warning("[Freyr/FinancialModelingPrep.py - company_balance_sheet] "+ str(symbol) +"$: " + str(err))
    except KeyError as err:
        logging.warning("[Freyr/FinancialModelingPrep.py - company_balance_sheet] "+ str(symbol) +"$: " + str(err))

    return buffer

def earnings(symbol):

    symbol = symbol.replace("-", ".")

    url = "https://financialmodelingprep.com/api/v3/financials/income-statement/" + str(symbol) + "?period=quarter"
    buffer = []
    count = 0
    try:
        data = get_jsonparsed_data(url)
        data = data['financials']
        for row in data:

            row_buffer = {}
            for column in row:
                if row[column] == '':
                    row_buffer[column] = 0
                else:
                    row_buffer[column] = row[column]

            buffer.append(row_buffer)

            count += 1

    except TypeError as err:
        logging.warning("[Freyr/FinancialModelingPrep.py - earnings] "+ str(symbol) +"$: " + str(err))
    except KeyError as err:
        logging.warning("[Freyr/FinancialModelingPrep.py - earnings] "+ str(symbol) +"$: " + str(err))

    return buffer