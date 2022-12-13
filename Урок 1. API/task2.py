import requests
import json
import time
from urllib.parse import urlencode
import hmac
import hashlib

API_KEY = 'C27BFADC8D6AA5D13EA8E36CA90708D4'
API_SECRET = 'f413ce0357c69992f4e5f47547be408c'


def get_info ():
    values = {}
    values['method'] = 'getInfo'
    values['nonce'] = str(int(time.time()))
    body = urlencode(values).encode('utf-8')
    sing = hmac.new(API_SECRET.encode('utf-8'), body, hashlib.sha512).hexdigest()
    url = 'https://yobit.net/api/3/ticker'

    headers = {
        'key': API_KEY,
        'sing': sing,
    }
    pairs = 'btc_usdt'
    p_url = '{}/{}'.format(url, pairs)
    response = requests.post(url=p_url, headers=headers, data=values)
    return response.json()

crypto = get_info()
with open('crypto.json', 'w', encoding='utf-8') as f:
    json.dump(crypto, f, ensure_ascii=False, indent=2)
print('Данные загружены!')