from web3 import Web3
from web3.providers.rpc import HTTPProvider
from web3.auto.gethdev import w3
from web3.middleware import geth_poa_middleware



# If you use one of the suggested infrastructure providers, the url will be of the form
# now_url  = f"https://eth.nownodes.io/{now_token}"
# alchemy_url = f"https://eth-mainnet.alchemyapi.io/v2/{alchemy_token}"
# infura_url = f"https://mainnet.infura.io/v3/{infura_token}"

def connect_to_eth():
    url = f"https://celo-mainnet.infura.io/v3/4a845c8000094d8f91e8bb909b20773a"
    w3 = Web3(HTTPProvider(url))
    assert w3.isConnected(), f"Failed to connect to provider at {url}"

    
    # inject the poa compatibility middleware to the innermost layer (0th layer)
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # confirm that the connection succeeded
    w3.clientVersion
    'Geth/v1.7.3-stable-4bb3c89d/linux-amd64/go1.9'
    return w3


if __name__ == "__main__":
    connect_to_eth()
