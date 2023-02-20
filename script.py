import requests
import json
import hmac
import hashlib
from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
#     print(data)
    # Extract TradingView alert parameters
    action = data['strategy']['order_action']
    contracts = data['strategy']['order_contracts']
    position = data['strategy']['position_size']
    symbol = 'BTCUSD'
    side = 'Buy' if action == 'buy' else 'Sell'
    quantity = contracts
    leverage = 10
    api_key = 'kIzg2mYU6Cpi9QPcIJ'
    secret_key = 'dYObTJ2yXtvM3ljePSOUpiU6UjA5q1qc2XAb'

    # Create order on Bybit API
    timestamp = int(time.time() * 1000)
    payload = {
        "api_key": api_key,
        "symbol": symbol,
        "side": side,
        "order_type": "Market",
        "qty": quantity,
        "time_in_force": "GoodTillCancel",
        "leverage": leverage,
        "timestamp": timestamp,
    }
    query_string = '&'.join([f"{k}={v}" for k, v in payload.items()])
    signature = hmac.new(secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    payload['sign'] = signature

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    url = 'https://api-testnet.bybit.com/v2/private/order/create'
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    return response.text

if __name__ == '__main__':
    app.run(port=5000, debug=True)
