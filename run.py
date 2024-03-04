# Import necessary functions/classes from your package
from src.auth.auth import generate_jwt_token
from src.websocket.coinbase_ws import run_websocket

def main():
    jwt_token = generate_jwt_token("GET", "/")
    run_websocket(jwt_token)

if __name__ == "__main__":
    main()
