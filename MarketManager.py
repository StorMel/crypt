from pubsub import publish
from TradingDTOs import *
from SolanaRpcApi import SolanaRpcApi
from RaydiumTokensMonitor import RaydiumTokensMonitor
import TokensApi as TokensApi
import Globals as globals
import time


# Manage Tokem Market Activities
class MarketManager(AbstractMarketManager):
    def __init__(self, solana_rpc_api: SolanaRpcApi):
        self.ray_pool_monitor = RaydiumTokensMonitor(solana_rpc_api)


        self.solana_rpc_api = solana_rpc_api
        self.ray_pool_monitor.start()

    def get_token_info(self, token_address: str) -> TokenInfo:
        ret_val = self.ray_pool_monitor.get_token_info(token_address)

        if not ret_val:
            ret_val = TokensApi.get_amm_token_pool_data(token_address,"EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v")

        return ret_val

    def get_price(self, token_address: str):
        token_info = self.ray_pool_monitor.get_token_info(token_address)

        if token_info:
            return token_info.price # with sol api
        else:
            # Get token information with raydium api
            lp_data = TokensApi.get_amm_token_pool_data(token_address,'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v')

            return lp_data.price



    async def monitor_token(self, token_address: str):
        await self.ray_pool_monitor.monitor_token(token_address)

    def _handle_token_update(self, arg1: str):
        new_price = self.get_price(arg1)
        new_price_string = f"{new_price:.20f}"
        print(arg1 + " was updated! Price: " + new_price_string)

