import hashlib
import hmac
import json
import requests
from pprint import pprint

# API info
API_HOST = 'https://api.bitkub.com'
API_KEY = '<API_KEY>'
API_SECRET = b'<API_SECRET>'

def json_encode(data):
	return json.dumps(data, separators=(',', ':'), sort_keys=True)

def sign(data):
	j = json_encode(data)
	print('Signing payload: ' + j)
	h = hmac.new(API_SECRET, msg=j.encode(), digestmod=hashlib.sha256)
	return h.hexdigest()

# check server time
response = requests.get(API_HOST + '/api/servertime')
ts = int(response.text)

# check balances
header = {
	'Accept': 'application/json',
	'Content-Type': 'application/json',
	'X-BTK-APIKEY': API_KEY,
}
data = {
	'sym': '<SYMBOL_CRYPTO>',
	'ts': ts,
}
signature = sign(data)
data['sig'] = signature

# My order history
response = requests.post(API_HOST + '/api/market/my-order-history', headers=header, data=json_encode(data))
response = response.json()
result = response['result']
for a in result:
	amount = a['amount']
	rate = a['rate']
	side = a['side']
	money = amount * rate
	if side == 'buy':
		print('----------------')
		print('BUY')
		print('จำนวนเหรียญ :',  amount)
		print('ราคา :', rate)
		print('เงินทุน :', money)
	else:
		print('----------------')
		print('SELL')
		print('จำนวนเหรียญ :',  amount)
		print('ราคา :', rate)
		print('ขายได้ :', money)


