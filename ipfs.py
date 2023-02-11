import requests
import json


def pin_to_ipfs(data):
	assert isinstance(data,dict), f"Error pin_to_ipfs expects a dictionary"
    # code here:
    return cid


def get_from_ipfs(cid,content_type="json"):
    assert isinstance(cid,str), f"get_from_ipfs accepts a cid in the form of a string"
    #code here:
    url_part = 'https://ipfs.infura.io:5001/api/v0/cat?arg='
    url = url_part + cid
    json_data = requests.get(url)
    data = json.loads(json_data)
	assert isinstance(data,dict), f"get_from_ipfs should return a dict"
	return data