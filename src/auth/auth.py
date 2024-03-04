import json
import hmac
import hashlib
import time
import requests
from requests.auth import AuthBase
from coinbase import jwt_generator  # Import the JWT generator module

# Set your API key and secret
API_KEY = 'organizations/4bf9d615-1d1c-40c5-8896-56572884d7e9/apiKeys/9d40b8f4-c0ba-4869-8599-a3bd8ae8757a'
API_SECRET = '-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEIFl4TVXnYh/p06W+4+LW3UeAlA+JT0kA5VPXVkEbe+10oAoGCCqGSM49\nAwEHoUQDQgAElfyad3FJnEIejeGEecgJZx2cnpFehWuQjhDtIOqiKfLhrL0BF1fz\nINx4Z1bC6usPILL7qrg+1ER5X4/8Ui6YqQ==\n-----END EC PRIVATE KEY-----\n'

# Create custom authentication for Coinbase API
class CoinbaseWalletAuth(AuthBase):
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    def __call__(self, request):
        timestamp = str(int(time.time()))
        message = timestamp + request.method + request.path_url + (request.body or '')
        signature = hmac.new(self.secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()

        request.headers.update({
            'CB-ACCESS-SIGN': signature,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'Content-Type': 'application/json'
        })
        return request


api_base_url = 'https://api.coinbase.com'


auth = CoinbaseWalletAuth(API_KEY, API_SECRET)

def generate_jwt_token(request_method, request_path):
    expiration_time = getattr(generate_jwt_token, 'expiration_time', 0)
    current_time = time.time()
    if current_time >= expiration_time:
        jwt_uri = jwt_generator.format_jwt_uri(request_method, request_path)
        jwt_token = jwt_generator.build_rest_jwt(jwt_uri, API_KEY, API_SECRET)
        generate_jwt_token.expiration_time = current_time + 120
        generate_jwt_token.token = jwt_token
    return generate_jwt_token.token

try:
    request_path = '/api/v3/brokerage/accounts'

    
    r = requests.get(api_base_url + request_path, headers={'Authorization': f'Bearer {generate_jwt_token("GET", request_path)}'})
    r.raise_for_status()  
    print(r.json()) 
except requests.exceptions.HTTPError as err:
    print("HTTP Error:", err)
except json.decoder.JSONDecodeError:
    print("Response does not contain valid JSON data.")
    print("Status code:", r.status_code)
