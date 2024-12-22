from jsonrpcclient import request, parse, Ok, Error
from solana.rpc.api import Client
from solana.rpc.types import TxOpts
from solders.pubkey import Pubkey
from solana.rpc.commitment import Confirmed, Processed, Finalized
from spl.token.constants import ASSOCIATED_TOKEN_PROGRAM_ID, TOKEN_PROGRAM_ID
from solders.transaction import VersionedTransaction
import requests

#https://solana.com/docs/rpc/websocket/accountsubscribe


class SolanaRpcApi:

    def __init__(self, rpc_uri, wss_uri):
        self.rpc_uri = rpc_uri
        self.wss_uri = wss_uri
        self.client = Client(self.rpc_uri)

    def run_rpc_method(self, request_name: str, params):
        json_request = request(request_name, params=params)
        response = requests.post(self.rpc_uri, json=json_request)

        parsed = parse(response.json())

        if isinstance(parsed, Error):
            return None
        else:
            return parsed



    def get_account_balance(self, account_address: str) -> float:
        response = self.run_rpc_method("getBalance", [account_address])

        if response:
            return response.result['value']
        else:
            return None



    def get_token_account_balance(self, associated_token_address: str):
        response = self.run_rpc_method("getTokenAccountBalance", [associated_token_address])

        if response:
            return response.result['value']['uiAmount']
        else:
            return None

    @staticmethod
    def get_associated_token_account_address(owner_address: str, mint_address: str) -> str:
        mint_address_pk = Pubkey.from_string(mint_address)
        owner_address_pk = Pubkey.from_string(owner_address)

        # Calculate the associated token address
        seeds = [bytes(owner_address_pk), bytes(TOKEN_PROGRAM_ID), bytes(mint_address_pk)]
        account_pubkey = Pubkey.find_program_address(seeds, ASSOCIATED_TOKEN_PROGRAM_ID)[0]

        return str(account_pubkey)



    @staticmethod
    def _extract_token_balance(owner_address: str, token_balance_dict: dict):
        for token_balance in token_balance_dict:
            if owner_address == token_balance['owner']:
                return token_balance

    @staticmethod
    def get_account_subscribe_request(account_address: str): #creating json web data to sent to the web socket
        return {
            "jsonrpc": "2.0",
            "id": 420,
            "method": "accountSubscribe",
            "params": [
                account_address,  # pubkey of account we want to subscribe to
                {
                    "encoding": "jsonParsed",  # base58, base64, base65+zstd, jsonParsed
                    "commitment": "confirmed",  # defaults to finalized if unset
                }
            ]
        }

        # Creates a transaction sub request

    @staticmethod
    def get_signature_request(signature: str):
        return {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "signatureSubscribe",
            "params": [
                signature,  # pubkey of account we want to subscribe to #TODO put in constructor
                {
                    "commitment": "confirmed",
                    "enableReceivedNotification": False
                }
            ]
        }