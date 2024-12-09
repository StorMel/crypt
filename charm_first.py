#pip install solana solders anchorpy
#pip install whirlpool-essentials

import asyncio
import time
import httpx

#https://github.com/everlastingsong/whirlpool-essentials?tab=readme-ov-file
from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from solders.keypair import Keypair

from orca_whirlpool.constants import ORCA_WHIRLPOOL_PROGRAM_ID
from orca_whirlpool.context import WhirlpoolContext
from orca_whirlpool.utils import PriceMath, DecimalUtil

#pool key search - https://www.orca.so/pools?tokens=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v&tokens=GFX1ZjR2P15tmrSwow6FjyDYcEkoFb4p4gJCpLBjaxHD
GOFX_USDC_WHIRLPOOL_PUBKEY = Pubkey.from_string("Cst4B1VGkirLHFW5iVUYYL3uc4Wys5uQVVnvNaYPs4XA")

async def main():
    RPC_ENDPOINT_URL = "https://api.mainnet-beta.solana.com"  ##main net: "https://api.mainnet-beta.solana.com" / /Devnet: "https://api.devnet.solana.com" /Testnet: "https://api.testnet.solana.com"
    connection = AsyncClient(RPC_ENDPOINT_URL)
    whirlpool_pubkey = GOFX_USDC_WHIRLPOOL_PUBKEY
    first_run=True

    while True:
      try:
        ctx = WhirlpoolContext(ORCA_WHIRLPOOL_PROGRAM_ID, connection, Keypair())
        whirlpool = await ctx.fetcher.get_whirlpool(whirlpool_pubkey)
        TimeStamp1 = await ctx.fetcher.get_latest_block_timestamp()
      except httpx.HTTPStatusError as e:
        print(f"Caught exception: {e}")
        if e.response.status_code == 429:  # Too many requests
         print("Rate limit reached, waiting to retry...")
         await asyncio.sleep(5)  # Wait for 5 seconds before retrying
        else:
         raise e  # Re-raise the error if it's not a 429

      if(first_run): # static data
            decimals_a = (await ctx.fetcher.get_token_mint(whirlpool.token_mint_a)).decimals  # USDC_DECIMAL
            decimals_b = (await ctx.fetcher.get_token_mint(whirlpool.token_mint_b)).decimals  # GOFX_DECIMAL


      tick_spacing = whirlpool.tick_spacing
      first_run = False

      current_tick_index = whirlpool.tick_current_index
      sqrt_price = whirlpool.sqrt_price
      current_price = PriceMath.sqrt_price_x64_to_price(sqrt_price, decimals_a, decimals_b)
      liquidity = whirlpool.liquidity  # Liquidity in the pool


    # Bid and ask price calculation
      bid_tick_index = current_tick_index - tick_spacing
      ask_tick_index = current_tick_index + tick_spacing

      bid_sqrt_price = PriceMath.tick_index_to_sqrt_price_x64(bid_tick_index)
      ask_sqrt_price = PriceMath.tick_index_to_sqrt_price_x64(ask_tick_index)

      bid_price = PriceMath.sqrt_price_x64_to_price(bid_sqrt_price, decimals_a, decimals_b)
      ask_price = PriceMath.sqrt_price_x64_to_price(ask_sqrt_price, decimals_a, decimals_b)
      price=float(DecimalUtil.to_fixed(current_price, decimals_b))
      Quantity = liquidity / price

      trade_data = {
        "latest block timestamp": TimeStamp1.timestamp,#int(time.time() * 1000)
        "timestamp": int(time.time() * 1000),
        "price": price,
        "quantity": Quantity,  # this wasnt the intention, i need to check the amount of swaps (trades) in a period of time
    }


      orderbook_data = {
            "bid": [float(DecimalUtil.to_fixed(bid_price, decimals_b))],
            "ask": [float(DecimalUtil.to_fixed(ask_price, decimals_b))],
        }

    # Print results
      print("Orderbook data:", orderbook_data)
      print("Trade data:", trade_data)


      await asyncio.sleep(2)




asyncio.run(main())
