#!/usr/bin/env python3

import requests
import json
import os
import hmac
import hashlib
import sys
import time
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode
from dotenv import load_dotenv

import csv

load_dotenv()
currencies = [ "jpy", "btc", "xem", "XYM", "ETH", "BCH", ]
methods = ["deposit_history", "withdraw_history"]

API = os.environ.get("ZAIF_API")
SECRET = os.environ.get("ZAIF_SECRET")

if len(sys.argv) < 2:
    print("Usage: ./deposit_withdraw year\nYear must be YYYY or all")
year = sys.argv[1]

with open('nonce') as f:
    nonce_read = f.readline()

nonce = int(nonce_read)

writer = csv.writer(sys.stdout)
writer.writerow(["Koinly Date", "Amount", "Currency"])

for coin in currencies:
    for method in methods:
        params = {
            'method': method,
            'currency': coin,
            'nonce': nonce,
        }
        encoded_params = urlencode(params)
        signature = hmac.new(bytearray(SECRET.encode('utf-8')), digestmod=hashlib.sha512)
        signature.update(encoded_params.encode('utf-8'))
        headers = {
            'key': API,
            'sign': signature.hexdigest()
        }
        response = requests.post('https://api.zaif.jp/tapi', data=encoded_params, headers=headers)
        if response.status_code != 200:
            raise Exception('return status code is {}'.format(response.status_code))
        nonce += 1
        with open('nonce', 'w') as f:
            f.write(str(nonce))
        d = json.loads(response.text)
        records = d['return']
        for k, v in records.items():
            ts = v['timestamp']
            amount = float(v['amount'])
            size = amount if method == "deposit_history" else -amount

            JST = timezone(timedelta(hours=+9), 'JST')
            dt = datetime.fromtimestamp(int(ts), tz=JST)
            utc = dt.astimezone(timezone.utc)
            if year == 'all' or utc.year == int(year):
                writer.writerow([utc.replace(tzinfo=None).isoformat(sep=' '), size, coin])


        time.sleep(7)