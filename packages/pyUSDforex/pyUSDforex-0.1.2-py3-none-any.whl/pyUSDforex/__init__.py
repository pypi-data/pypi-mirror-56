import requests
import json
from threading import Lock
import shelve
import time
from decimal import *


def convert(amount, to_currency, app_id):

    mutex = Lock()

    # lock the thread
    mutex.acquire()

    # open shelve
    exchange_shelve = shelve.open('latest_exchange.db')

    # first we need to check if the shelve exists
    if 'latest' not in exchange_shelve:
        exchange_shelve['latest'] = __fetch_rates(app_id)

    # check if the shelved result is from the past hour
    if (int(time.time()) - exchange_shelve['latest']['timestamp']) > 3900:
        exchange_shelve['latest'] = __fetch_rates(app_id)
        rates = exchange_shelve['latest']['rates']
    else:
        # get the result from the shelve
        rates = exchange_shelve['latest']['rates']

    # close the shelve
    exchange_shelve.close()

    # unlock the thread
    mutex.release()

    # solve for the result
    try:
        result = (1 / Decimal(rates[to_currency]) * Decimal(amount))
    except KeyError:
        error_msg = 'The exchange rate for '+to_currency+' cannot be found.'
        raise Exception(error_msg)
    return result


def __fetch_rates(app_id):

    # get the json exchange rates to USD
    request_url = 'https://openexchangerates.org/api/latest.json?app_id='+app_id+'&base=USD&prettyprint=false'

    req_ob = requests.get(request_url)

    return req_ob.json()
