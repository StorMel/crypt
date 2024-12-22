from enum import Enum
from abc import abstractmethod



class TokenInfo:
    def __init__(self, token_address):
        self.token_address = token_address
        self.market_id = ''
        self.price = 0
        self.token_vault_ui_amount = 0
        self.sol_vault_address = ''
        self.token_vault_address = ''
        self.sol_address = ''
        self.token_decimals = ''
        self.decimals_scale_factor = 0
        self.vol=0
        self.priceMin=0
        self.priceMax=0



class AbstractMarketManager:
    @abstractmethod
    def get_price(self, token_address: str) -> float:
        pass

