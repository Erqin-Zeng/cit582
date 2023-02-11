import requests
import json


def pin_to_ipfs(data):
    assert isinstance(data, dict), f"Error pin_to_ipfs expects a dictionary"
    # code here:
    json_data = json.dumps(data)
    files = {'file':json_data}
    # infura_url = "https://ipfs.infura.io/ipfs/"
    # url = f'{infura_url}{project_id}'
    infura_url = 'https://ipfs.infura.io:5001/api/v0/add'
    project_id = "2La77rgcqFxHLaq1C2Q9JggeJzF"
    project_secret = 'fc4db061014f8f7db76ae4ca4c152ac3'
    response = requests.post(infura_url, files=files, auth=(project_id, project_secret))
    p = response.json()
    cid = p['Hash']
    return cid


def get_from_ipfs(cid, content_type="json"):
    assert isinstance(cid, str), f"get_from_ipfs accepts a cid in the form of a string"
    # code here:
    params = (('arg', cid),)
    project_id = "2La77rgcqFxHLaq1C2Q9JggeJzF"
    project_secret = 'fc4db061014f8f7db76ae4ca4c152ac3'
    response = requests.post('https://ipfs.infura.io:5001/api/v0/cat', params=params, auth=(project_id, project_secret))
    print(response)
    data = json.loads(response.text)
    assert isinstance(data, dict), f"get_from_ipfs should return a dict"
    return data
