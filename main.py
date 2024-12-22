from MarketManager import MarketManager
from SolanaRpcApi import SolanaRpcApi
from TradingDTOs import *
import TokensApi as tok
import asyncio
import time


async def main():
    http_uri = "https://api.mainnet-beta.solana.com"
    wss_uri = "wss://api.mainnet-beta.solana.com"
    #this isnt really being used


    solana_rpc_api = SolanaRpcApi(http_uri, wss_uri)
    market_manager = MarketManager(solana_rpc_api)




    token_address = "GFX1ZjR2P15tmrSwow6FjyDYcEkoFb4p4gJCpLBjaxHD"#GOFX
    # the usdc address is hardcoded rn in the marketmanager
    while True:

        token=market_manager.get_token_info(token_address)
        price = token.price
        vol = token.vol
        price_min = token.priceMin
        price_max =token.priceMax

        trade_data = {
            "timestamp": int(time.time() * 1000),
            "price": price,
            "day vol": vol,
        }

        orderbook_data = {
            "bid": [price_min],
            "ask": [price_max],
        }

        # Print results
        print("Orderbook data:", orderbook_data)
        print("Trade data:", trade_data)


asyncio.run(main())