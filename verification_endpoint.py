from flask import Flask, request, jsonify
from flask_restful import Api
import json
import eth_account
import algosdk

app = Flask(__name__)
api = Api(app)
app.url_map.strict_slashes = False

@app.route('/verify', methods=['GET','POST'])
def verify():
    content = request.get_json(silent=True)
    print (content)
    #Check if signature is valid

    #ethoereum
    if content["payload"]["platform"] == 'Ethereum':
        eth_pk = content.payload.pk
        payload = content.payload
        eth_encoded_msg = eth_account.messages.encode_defunct(text=payload)
        eth_sig_obj = content.sig

        if eth_account.Account.recover_message(eth_encoded_msg, signature=eth_sig_obj.signature.hex()) == eth_pk:
            result = True  # Should only be true if signature validates
            return jsonify(result)

    # Algorand
    if content.payload.platform == 'Algorand':
        payload = content.payload
        algo_pk = content.payload.pk
        algo_sig_str = content.sig

        if algosdk.util.verify_bytes(payload.encode('utf-8'), algo_sig_str, algo_pk):
            result = True  # Should only be true if signature validates
            return jsonify(result)
    
    result = False  # Should only be true if signature validates
    return jsonify(result)
    
if __name__ == '__main__':
    app.run(port='5002')
