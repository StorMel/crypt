
from TradingDTOs import TokenInfo
import requests


#https://api-v3.raydium.io/docs/#/


def get_request(request_uri: str):
    response = requests.get(request_uri)

    if response.status_code == 200:
        return response.json()
    else:
        return None


# Retrieve a token't liquidity pool data using the Raydium v3 API
def get_amm_token_pool_data(token_address1: str,token_address2: str) -> TokenInfo:
    ray_uri = "https://api-v3.raydium.io/pools"
    ray_uri_marketid_uri = ray_uri + "/info/mint?mint1=" + token_address1 + "&mint2=" + token_address2 + "&poolType=all&poolSortField=default&sortType=desc&pageSize=1&page=1"
   #GFX1ZjR2P15tmrSwow6FjyDYcEkoFb4p4gJCpLBjaxHD
   # 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v'


    # Make the API call
    data = get_request(ray_uri_marketid_uri)
    #print(data)
    if len(data) > 0:
        try:
            token_info = TokenInfo(token_address1)
            token_info.market_id = data['data']['data'][0]['id']
            token_info.price = data['data']['data'][0]['price']
            token_info.vol=data['data']['data'][0]['day']['volume']
            token_info.priceMin = data['data']['data'][0]['day']['priceMin']
            token_info.priceMax = data['data']['data'][0]['day']['priceMax']





            ##lq data
            pool_info_uri = ray_uri + "/key/ids?ids=" + token_info.market_id
            data = get_request(pool_info_uri)

            if len(data)>0:
                token_info.sol_vault_address =data['data'][0]['vault']['A']
                token_info.token_vault_address= data['data'][0]['vault']['B']

        except Exception as e:
            print(str(e))

    return  token_info


