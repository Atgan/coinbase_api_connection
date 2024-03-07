import json
from coinbase import jwt_generator  
import uuid
import http.client



api_key = 'organizations/4bf9d615-1d1c-40c5-8896-56572884d7e9/apiKeys/31e57904-4d28-4d17-b2ae-7480559725d5'
api_secret = '-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEINlQRo2++kJamgT0LogsL4Nj4YHyqEYDYZtjC7RY7vMroAoGCCqGSM49\nAwEHoUQDQgAEFGUQU0yDBGNtwLmsF+8H5I0gbF+hWhXhQKolVtCwhnyf0c+sEv5c\nSTn18ck0Q20WvmEHjIUBTm361+aTawwtdA==\n-----END EC PRIVATE KEY-----\n'
request_method = "POST"
request_path = "/api/v3/brokerage/orders"



def generate_jwt_token(request_path, request_method):
    jwt_uri = jwt_generator.format_jwt_uri(request_method, request_path)
    jwt_token = jwt_generator.build_rest_jwt(jwt_uri, api_key, api_secret)
    return jwt_token

def make_request():
    request_path = '/api/v3/brokerage/accounts'
    request_method = 'GET'
    jwt_token = generate_jwt_token()
    headers = {
        'Authorization': f'Bearer {jwt_token}'
    }

    conn = http.client.HTTPSConnection('api.coinbase.com')
    conn.request(request_method, request_path, headers=headers)
    response = conn.getresponse()
    data = response.read()
    print(data.decode("utf-8"))


def buy_btc(amount_usd, amount_btc, unique_order_id):
    request_path = '/api/v3/brokerage/orders'
    request_method = 'POST'
    jwt_token = generate_jwt_token(request_path, request_method)
    headers = {
        'Authorization': f'Bearer {jwt_token}'
    }
    payload = {
        
        'client_order_id': 'testm1',
        'product_id': 'BTC-USD',
        'side': 'BUY',
        'order_configuration': {
            'market_market_ioc': {
                'quote_size': '5',  # Specify the amount of USD you want to spend
            }
        }
    }
    payload_str = json.dumps(payload)
    conn = http.client.HTTPSConnection('api.coinbase.com')
    conn.request(request_method, request_path, payload_str, headers=headers)
    response = conn.getresponse()
    data = response.read()
    print(data.decode("utf-8"))


    
 

if __name__ == "__main__":
    unique_order_id = "testj" #provide this-you can pass this to get details on a trage etc
    amount_btc=str('0.00007465')
    amount_usd=str('5')
    buy_btc(amount_btc,amount_usd, unique_order_id)
   
