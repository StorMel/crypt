from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey as PublicKey
from solders.rpc.responses import GetAccountInfoResp
import base64
import asyncio
import time  # Importing the time module to fetch the current timestamp

# Replace with your liquidity pool address
LIQUIDITY_POOL_ADDRESS = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"#"C3b5AWQJiyar5g8EWu75zgDE26F55ZJWpqtFVCCVDQQQ"

# Replace with the Serum market address for order book (example: USDC/USDT)
MARKET_ADDRESS = "8VTHXk6kXK6QpY6Xg3bV9jNUBy6pbbUddZXsE8bHwtzP"  # Replace with actual Serum market address


async def get_token_value_volume_and_orderbook(pool_address: str, market_address: str):
    # Connect to the Solana RPC client
    rpc_client = AsyncClient("https://api.mainnet-beta.solana.com")

    # Fetch account information for the liquidity pool
    pool_pubkey = PublicKey.from_string(pool_address)
    response: GetAccountInfoResp = await rpc_client.get_account_info(pool_pubkey)

    if not response.value:
        print("Failed to fetch liquidity pool account data.")
        await rpc_client.close()
        return

    # Decode account data
    account_data = response.value.data
    if isinstance(account_data, tuple):  # Base64 encoded
        raw_data = base64.b64decode(account_data[0])
    else:
        raw_data = account_data

    # Decode the pool data
    reserve_1, reserve_2, volume = decode_pool_data(raw_data)

    # Calculate token value using reserve balances
    token_value = calculate_token_value(reserve_1, reserve_2)

    # Get the current timestamp
    current_timestamp = int(time.time())  # Get the current time in seconds

    # Fetch the orderbook data (Bid/Ask prices)
    bid_price, ask_price = await fetch_orderbook_data(rpc_client, market_address)

    print(f"trading data - Timestamp: {current_timestamp}, Token Value: {token_value}, Pool Volume: {volume}")
    print(f"Orderbook Data - Bid: {bid_price}, Ask: {ask_price}")

    await rpc_client.close()
    await asyncio.sleep(2)

async def fetch_orderbook_data(rpc_client: AsyncClient, market_address: str):
    # Fetch the orderbook for the market using Serum
    market_pubkey = PublicKey.from_string(market_address)

    # Get the order book data for the market
    orderbook_data = await rpc_client.get_account_info(market_pubkey)

    if not orderbook_data.value:
        print("Failed to fetch orderbook data.")
        return None, None

    # Decode order book data
    account_data = orderbook_data.value.data
    if isinstance(account_data, tuple):  # Base64 encoded
        raw_data = base64.b64decode(account_data[0])
    else:
        raw_data = account_data

    # Placeholder for parsing orderbook data. This step depends on the specific layout of the order book.
    # Typically, the order book has bid and ask price arrays that you need to parse.
    bid_price, ask_price = decode_orderbook_data(raw_data)

    return bid_price, ask_price


def decode_pool_data(raw_data):
    """
    Decode the liquidity pool account data.
    Assumes the following structure:
    - Offset 0-8: Reserve 1 (token A)
    - Offset 8-16: Reserve 2 (token B)
    - Offset 16-24: Pool volume
    Adjust offsets based on the specific program layout.
    """
    reserve_1 = int.from_bytes(raw_data[0:8], "little")
    reserve_2 = int.from_bytes(raw_data[8:16], "little")
    volume = int.from_bytes(raw_data[16:24], "little")  # Replace with actual offset for volume
    return reserve_1, reserve_2, volume


def decode_orderbook_data(raw_data):
    """
    Decode the orderbook data. This is a placeholder that assumes bid and ask prices are in raw_data.
    You need to adjust this parsing based on the actual format of the orderbook.
    """
    # Placeholder decoding. Replace with actual parsing logic for Serum's orderbook
    # Serum's orderbook structure might contain bid/ask prices as arrays. Here we'll just return mock values.

    bid_price = 1.23  # Example: Highest bid price
    ask_price = 1.25  # Example: Lowest ask price

    return bid_price, ask_price


def calculate_token_value(reserve_1, reserve_2):
    # Implement token value calculation logic
    # For simplicity, assume reserve_1 is token A and reserve_2 is token B
    return reserve_2 / reserve_1  # Example: Token B value in terms of Token A


# Run the script
if __name__ == "__main__":
    while True:
     asyncio.run(get_token_value_volume_and_orderbook(LIQUIDITY_POOL_ADDRESS, MARKET_ADDRESS))
