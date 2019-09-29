# import all needed modules;
from bs4 import BeautifulSoup
from decimal import *
import requests


# main converted function;
def convert(amount, cur_from, cur_to, date):

    http = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + date   # address for our request;
    response = requests.get(http)
    soup = BeautifulSoup(response.content, "xml")   # BeautifulSoup object;

    # check if base value is a RUR, unless find the currency for currency_from;
    if cur_from == "RUR":
        currency_from = 1
        nominal_from = 1
    else:
        currency_from = soup.find('CharCode', text=cur_from).find_next_sibling('Value').string.replace(',', '.')
        nominal_from = soup.find('CharCode', text=cur_from).find_next_sibling('Nominal').string
    currency_to = soup.find('CharCode', text=cur_to).find_next_sibling('Value').string.replace(',', '.')
    nominal_to = soup.find('CharCode', text=cur_to).find_next_sibling('Nominal').string

    # convert from string to make calculation;
    currency_from = Decimal(currency_from)
    currency_to = Decimal(currency_to)
    nominal_from = Decimal(nominal_from)
    nominal_to = Decimal(nominal_to)

    # calculation;
    converted = (currency_from / nominal_from) / (currency_to / nominal_to) * amount

    # we should catch error if there are less than four digit after zero;
    bool_var = True
    pattern = '.0000'

    while bool_var:
        try:
            converted = converted.quantize(Decimal(pattern), rounding=ROUND_UP)
        except:
            pattern = pattern[:len(pattern) - 1]
        else:
            bool_var = False

    # define result;
    results = converted
    return results


result = convert(Decimal('1000.1000'), 'RUR', 'JPY', "17/02/2005")
print(result)
