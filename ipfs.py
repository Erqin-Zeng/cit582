import requests
import json

def pin_to_ipfs(data):
    assert isinstance(data, dict), f"Error pin_to_ipfs expects a dictionary"
    # code here:
    json_data = json.dumps(data)
    infura_url = "https://ipfs.infura.io/ipfs/"
    project_id = "2La77rgcqFxHLaq1C2Q9JggeJzF"
    url = f'{infura_url}{project_id}'
    response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json_data.encode("utf-8"))
    p = json.loads(response.text)
    cid = p['Hash']
    return cid


def get_from_ipfs(cid, content_type="json"):
    assert isinstance(cid, str), f"get_from_ipfs accepts a cid in the form of a string"
    # code here:
    infura_url = "https://ipfs.infura.io:5001/api/v0/cat?arg="
    url = f'{infura_url}{cid}'
    json_data = requests.get(url)
    data = json.loads(json_data.text)
    assert isinstance(data, dict), f"get_from_ipfs should return a dict"
    return data
