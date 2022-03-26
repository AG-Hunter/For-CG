import csv
import time
import hashlib
import hmac
import requests
import api_keys

def fetch_price(token):
    pair = token + '_USDT'
    host = "https://api.gateio.ws"
    prefix = "/api/v4"
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    url = '/spot/tickers'
    query_param = '?' + 'currency_pair=' + str(pair)
    sign_headers = gen_sign('GET', prefix + url, query_param)
    headers.update(sign_headers)
    r = requests.request('GET', host + prefix + url + query_param, headers=headers)
    return r.json()

def fetch_spot_balances():
    host = "https://api.gateio.ws"
    prefix = "/api/v4"
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    url = "/spot/accounts"
    sign_headers = gen_sign('GET', prefix+url)
    headers.update(sign_headers)
    r = requests.request('GET', host + prefix + url, headers=headers)
    return r.json()

def fetch_sub_account_balances():
    host = "https://api.gateio.ws"
    prefix = "/api/v4"
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    url = '/wallet/sub_account_balances'
    sign_headers = gen_sign('GET', prefix+url)
    headers.update(sign_headers)
    r = requests.request('GET', host + prefix + url, headers=headers)
    return r.json()

# Generates headers that are used in the API call in 'fetch_trades'
def gen_sign(method, url, query_string=None, payload_string=None):
    key = api_keys.gate_keys()[0]
    secret = api_keys.gate_keys()[1]
    t = time.time()
    m = hashlib.sha512()
    m.update((payload_string or "").encode('utf-8'))
    hashed_payload = m.hexdigest()
    s = '%s\n%s\n%s\n%s\n%s' % (method, url, query_string or "", hashed_payload, t)
    sign = hmac.new(secret.encode('utf-8'), s.encode('utf-8'), hashlib.sha512).hexdigest()
    return {'KEY': key, 'Timestamp': str(t), 'SIGN': sign}

def export_balances():
    token_list = []
    balance_list = []
    last_price_lst =[]
    USDT_bal_lst =[]
    spot = fetch_spot_balances()
    for entry in spot:
        token = entry['currency']
        token_list.append(token)
        balance = entry['available']
        balance_list.append(entry['available'])
        try:
            last_price = fetch_price(token)
            last_price = last_price[0]['last']
            last_price_lst.append(last_price)
        except:
            if token == "USDT":
                last_price = '1'
                last_price_lst.append("1")
            else:
                last_price_lst.append('N/A')
        try:
            USDT_bal = float(balance) * float(last_price)
            USDT_bal_lst.append(USDT_bal)
        except:
            USDT_bal_lst.append("NA")

    new_lst = [list(x) for x in zip(token_list, balance_list,last_price_lst , USDT_bal_lst)]
    with open('daily_balance_update.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['Token', 'Balance', 'Last Price', 'USDT Balance'])
        for entry in new_lst:
            filewriter.writerow(entry)
    print('Data export is complete!')

export_balances()