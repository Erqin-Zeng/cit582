from web3 import Web3
from web3.contract import Contract
from web3.providers.rpc import HTTPProvider
import requests
import json
import time

bayc_address = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
contract_address = Web3.toChecksumAddress(bayc_address)

#You will need the ABI to connect to the contract
#The file 'abi.json' has the ABI for the bored ape contract
#In general, you can get contract ABIs from etherscan
#https://api.etherscan.io/api?module=contract&action=getabi&address=0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D
with open('/home/codio/workspace/abi.json', 'r') as f:
	abi = json.load(f) 

############################
#Connect to an Ethereum node
api_url = "https://mainnet.infura.io/v3/4a845c8000094d8f91e8bb909b20773a"
provider = HTTPProvider(api_url)
web3 = Web3(provider)

def get_ape_info(apeID):
    assert isinstance(apeID, int), f"{apeID} is not an int"
    assert 1 <= apeID <= 10000, f"{apeID} must be between 1 and 10,000"

    data = {'owner': "", 'image': "", 'eyes': "" }

    try:
        # Create contract instance
        contract = web3.eth.contract(address=contract_address, abi=abi)

        # Call the contract function to get Ape information
        result = contract.functions.getApeInfo(apeID).call()

        # Parse the result and set data
        data['owner'] = result[0]
        data['image'] = f"https://gateway.pinata.cloud/ipfs/{result[1]}/{apeID}"
        data['eyes'] = result[2]

    except Exception as e:
        print(f"Error fetching Ape info for ID {apeID}: {str(e)}")

    assert isinstance(data, dict), f'get_ape_info({apeID}) should return a dict'
    assert all([a in data.keys() for a in ['owner', 'image', 'eyes']]), f"return value should include the keys 'owner','image' and 'eyes'"
    
    return data


