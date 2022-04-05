import base64
import hmac
import hashlib
import api_keys
import time
import requests
import csv

def hmac_sha256(secret, pre_hash_msg):
    return hmac.new(secret.encode('utf-8'), pre_hash_msg.encode('utf-8'), hashlib.sha256).digest()

def get_signature(secret, timestamp):
    pre_hash_msg = timestamp + 'balance'
    return base64.b64encode(hmac_sha256(secret, pre_hash_msg)).decode('utf-8')

def gen_sign():
    key = api_keys.ascendex_keys()[0]
    secret = api_keys.ascendex_keys()[1]
    timestamp = str(int(time.time() * 1000))
    signature = get_signature(secret, timestamp)
    headers = {"Accept": "application/json", "Content-Type": "application/json", "x-auth-key": key, "x-auth-signature": signature, "x-auth-timestamp": timestamp}
    return headers

def api_call():
    headers = gen_sign()
    api_path = 'cash/balance'
    url = 'https://ascendex.com/4/api/pro/v1/' + api_path
    response = requests.request('get', url, headers=headers)
    dict_response = response.json()
    return dict_response

def fetch_price(token):
    pair = token + '/USDT'
    url = 'https://ascendex.com/api/pro/v1/spot/ticker'
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    query_param = '?' + 'symbol=' + str(pair)
    r = requests.request('GET', url + query_param, headers=headers)
    return r.json()

def fetch_spot_balances():
    response_dict = api_call()
    currency_list = []
    balance_list = []
    info = response_dict['data']
    for entry in info:
        currency = entry['asset']
        currency_list.append(currency)
        balance = entry['totalBalance']
        balance_list.append(balance)
    return currency_list, balance_list

def export_balances():
    last_price_lst =[]
    USDT_bal_lst =[]
    currency_list, balance_list = fetch_spot_balances()
    for token in currency_list:
        try:
            last_price = fetch_price(token)
            last_price = last_price['data']['close']
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
