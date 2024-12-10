import asyncio
from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey  # Newer solana versions
from solders.keypair import Keypair
from solders.rpc.responses import GetAccountInfoResp
import base64
import struct

async def main():
    async with AsyncClient("https://api.devnet.solana.com") as client:
        res = await client.is_connected()
    print(res)  # True

    # Alternatively, close the client explicitly instead of using a context manager:
    client = AsyncClient("https://api.devnet.solana.com")
    res = await client.is_connected()
    print(res)  # True
    await client.close()

asyncio.run(main())



# Define an async function to handle the async operations
async def get_balance():
    con = AsyncClient(RPC_ENDPOINT_URL)
    balance = await con.get_balance(GOFX_USDC_PUBKEY)  # Await the coroutine
    print(balance)
    await con.close()  # Close the connection after the operation

def decode_serum_orderbook(raw_data):
    # Decode Base64 if necessary
    if isinstance(raw_data, bytes):
        data = raw_data
    else:
        data = base64.b64decode(raw_data)

    header_size = 40  # SLAB header size in bytes
    slab_data = data[header_size:]  # Skip header to start of SLAB

    orders = []
    entry_size = 80  # Estimated size for each order entry (depends on SLAB spec)

    while len(slab_data) >= entry_size:
        # Unpack each entry
        price, size, _, _, owner = struct.unpack("<QQ16s16s32s", slab_data[:entry_size])
        orders.append({
            "price": price / 1e6,  # Adjust for decimals
            "size": size,
            "owner": owner.hex()  # Convert bytes to hex
        })
        slab_data = slab_data[entry_size:]  # Move to the next entry

    return orders



## Serum market addresses (replace with your market address)
#BIDS_PUBKEY = Pubkey.from_string("BIDS_ADDRESS_HERE")  # Replace with Serum bids account address
#ASKS_PUBKEY = Pubkey.from_string("ASKS_ADDRESS_HERE")  # Replace with Serum asks account address
GOFX_USDC_PUBKEY = Pubkey.from_string("Cst4B1VGkirLHFW5iVUYYL3uc4Wys5uQVVnvNaYPs4XA")
RPC_ENDPOINT_URL = "https://api.mainnet-beta.solana.com"

async def fetch_orderbook():
    # Connect to Solana RPC
    client = AsyncClient(RPC_ENDPOINT_URL)

    # Fetch the bids account info
    #bids_resp: GetAccountInfoResp = await client.get_account_info(BIDS_PUBKEY)
    #if not bids_resp.value:
        #print("Failed to fetch bids account.")
       # return

    # Fetch the asks account info
    #asks_resp: GetAccountInfoResp = await client.get_account_info(ASKS_PUBKEY)
    #if not asks_resp.value:
     #   print("Failed to fetch asks account.")
      #  return

    price: GetAccountInfoResp = await client.get_account_info(GOFX_USDC_PUBKEY)
    if not price.value:
        print("Failed to fetch price account.")
        return
    # Process raw order book data (you'll need to decode Serum-specific data structures)
    #print("Raw bids data:", bids_resp.value.data)
    #print("Raw asks data:", asks_resp.value.data)
    data=price.value.data
    print("Raw asks data:", data)
    decoded_orders=decode_serum_orderbook(data)
    print(decoded_orders)
    for order in decoded_orders:
        print(f"Price: {order['price']}, Size: {order['size']}, Owner: {order['owner']}")
    # Close the client connection
    await client.close()

# Run the async function
asyncio.run(fetch_orderbook())

