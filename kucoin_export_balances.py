import requests
import hmac
import time
import hashlib
import base64
import api_keys
import csv

def get_keys():
    api_key = api_keys.kucoin_keys()[0]
    api_secret = api_keys.kucoin_keys()[1]
    api_passphrase = api_keys.kucoin_keys()[2]
    return api_key, api_secret, api_passphrase

def gen_sign():
    key, secret, passphrase = get_keys()
    now = int(time.time() * 1000)
    str_to_sign = str(now) + 'GET' + '/api/v1/accounts'
    signature = base64.b64encode(
        hmac.new(secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(
        hmac.new(secret.encode('utf-8'), passphrase.encode('utf-8'), hashlib.sha256).digest())
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2"
    }
    return headers

def construct_query(token = ''):
        url = 'https://api.kucoin.com/api/v1/accounts' + token
        return url

def api_call():
    url = construct_query()
    headers = gen_sign()
    response = requests.request('get', url, headers=headers)
    dict_response = response.json()
    return dict_response

def fetch_spot_balances():
    response_dict = api_call()
    currency_list = []
    balance_list = []
    info = response_dict['data']
    for entry in info:
        currency = entry['currency']
        currency_list.append(currency)
        balance = entry['balance']
        balance_list.append(balance)
    return currency_list, balance_list

def fetch_price(token):
    pair = token + '-USDT'
    host = "https://api.kucoin.com"
    prefix = "/api/v1/"
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    url = 'market/orderbook/level1'
    query_param = '?' + 'symbol=' + str(pair)
    r = requests.request('GET', host + prefix + url + query_param, headers=headers)
    return r.json()

def export_balances():
    last_price_lst =[]
    USDT_bal_lst =[]
    currency_list, balance_list = fetch_spot_balances()
    for token in currency_list:
        try:
            last_price = fetch_price(token)
            last_price = last_price["data"]['price']
            last_price_lst.append(last_price)
        except:
            if token == "USDT":
                last_price_lst.append("1")
            else:
                last_price_lst.append('N/A')
    try:
        for num in list(range(len(balance_list))):
            USDT_bal = float(last_price_lst[num]) * float(balance_list[num])
            USDT_bal_lst.append(USDT_bal)
    except:
        USDT_bal_lst.append("NA")

    new_lst = [list(x) for x in zip(currency_list, balance_list, last_price_lst, USDT_bal_lst)]
    with open('daily_balance_update.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['Token', 'Balance', 'Last Price', 'USDT Balance'])
        for entry in new_lst:
            filewriter.writerow(entry)
    print('Data export is complete! \nAG Hunter is awesome!')

export_balances()