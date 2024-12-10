#https://github.com/michaelhly/solana-py
from solana.rpc.api import Client
from solders.pubkey import Pubkey  # Newer solana versions
import http.client
import json

# Initialize Solana RPC Client
solana_client = Client("https://api.mainnet-beta.solana.com")

# Serum market address for GOFX/USDC
GOFX_USDC_MARKET = Pubkey.from_string("Cst4B1VGkirLHFW5iVUYYL3uc4Wys5uQVVnvNaYPs4XA")
print(GOFX_USDC_MARKET)

def get_order_book(market_address: Pubkey):
    # Serum API endpoint
    host = "api.serum-vial.dev"
    path = f"/v1/markets/{market_address}"

    # Establish connection and send GET request
    connection = http.client.HTTPSConnection(host)
    connection.request("GET", path)

    # Get response
    response = connection.getresponse()
    if response.status == 200:
        data = response.read()
        return json.loads(data)  # Parse JSON response
    return None

# Get the order book for GOFX/USDC
order_book = get_order_book(GOFX_USDC_MARKET)
if order_book:
    print("Bid/Ask Data:", order_book['data']['orderbook'])
    print("Volume (24h):", order_book['data']['volume24hr'])
else:
    print("Failed to fetch order book data.")
