import requests
import requests_cache
import json
import time
from decimal import *


def convert(amount, to_currency, app_id):

    exchange_obj = __fetch_rates(app_id)

    rates = exchange_obj['rates']

    # solve for the result
    try:
        result = (1 / Decimal(rates[to_currency]) * Decimal(amount))
    except KeyError:
        error_msg = 'The exchange rate for '+to_currency+' cannot be found.'
        raise Exception(error_msg)
    return result


def __fetch_rates(app_id):

    expire_after = timedelta(hours=1)
    requests_cache.install_cache(expire_after=expire_after)

    # get the json exchange rates to USD
    request_url = 'https://openexchangerates.org/api/latest.json?app_id='+app_id+'&base=USD&prettyprint=false'

    req_ob = requests.get(request_url)

    return req_ob.json()
