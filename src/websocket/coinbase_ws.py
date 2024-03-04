import websocket 
import json
from src.auth.auth import generate_jwt_token

def on_message(ws, message):
    print(json.loads(message))

def on_error(ws, error):
    print(error)

def on_close(ws, *args):
    print("### closed ###")

def on_open(ws, jwt_token):
    print("### open ###")
    send_auth_headers(ws)  # Call send_auth_headers function when connection is opened
    subscribe_message = {
        "type": "subscribe",
        "channels": [{"name": "ticker", "product_ids": ["BTC-USD"]}]
    }
    ws.send(json.dumps(subscribe_message))

def send_auth_headers(ws):
    jwt_token = run_websocket.jwt_token
    ws.header = {'Authorization', 'Bearer ' + jwt_token}

def run_websocket(jwt_token):
    run_websocket.jwt_token = jwt_token
    ws = websocket.WebSocketApp("wss://ws-feed.exchange.coinbase.com",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close  
                                )
    ws.on_open = lambda ws: on_open(ws, jwt_token)  
    ws.run_forever()
