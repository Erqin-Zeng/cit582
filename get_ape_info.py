from web3 import Web3
from web3.contract import Contract
from web3.providers.rpc import HTTPProvider
import requests
import json
import time

bayc_address = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
contract_address = Web3.toChecksumAddress(bayc_address)

# Load the ABI
with open('/home/codio/workspace/abi.json', 'r') as f:
  abi = json.load(f)

# Connect to an Ethereum node
api_url = "https://mainnet.infura.io/v3/4a845c8000094d8f91e8bb909b20773a"
provider = HTTPProvider(api_url)
web3 = Web3(provider)

# Create a contract instance
contract = web3.eth.contract(address=contract_address, abi=abi)

def get_ape_info(apeID):
    assert isinstance(apeID, int), f"{apeID} is not an int"
    assert 1 <= apeID <= 10000, f"{apeID} must be between 1 and 10,000"

    data = {'owner': "", 'image': "", 'eyes': "" }

    try:
        # Get the owner's address
        owner = contract.functions.ownerOf(apeID).call()
        data['owner'] = owner

        # Get the tokenURI
        tokenURI = contract.functions.tokenURI(apeID).call()
        
        # Replace 'ipfs://' with the IPFS gateway URL
        tokenURI = tokenURI.replace('ipfs://', 'https://gateway.pinata.cloud/ipfs/')

        data['image'] = tokenURI

        # Fetch additional data from IPFS if needed
        response = requests.get(tokenURI)
        if response.status_code == 200:
            print("here")
            ipfs_data = response.json()
            if 'eyes' in ipfs_data:
                print("here2")
                data['eyes'] = ipfs_data['Eyes']

    except Exception as e:
        print(f"Error fetching data for Ape {apeID}: {str(e)}")

    assert isinstance(data, dict), f'get_ape_info({apeID}) should return a dict'
    assert all([a in data.keys() for a in ['owner', 'image', 'eyes']]), f"Return value should include the keys 'owner', 'image', and 'eyes'"
  
    # Print the result
    print(f"Ape {apeID} Info:")
    print("'owner':", data['owner'],)
    print("'image':", data['image'],)
    print("'eyes':", data['eyes'])
    return data
