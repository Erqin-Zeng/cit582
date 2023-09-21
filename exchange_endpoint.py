# These decorators allow you to use g.session to access the database inside the request code
@app.before_request
def create_session():
    g.session = scoped_session(DBSession)

@app.teardown_appcontext
def shutdown_session(response_or_exc):
    g.session.commit()
    g.session.remove()

@app.route('/verify', methods=['GET','POST'])
def verify():
    content = request.get_json(silent=True)
    #print (content["payload"]["platform"])
    #print (content)
    #Check if signature is valid

    #ethoereum
    if content["payload"]["platform"] == 'Ethereum':       
        payload = content["payload"]
        eth_pk = payload["sender_pk"]
        eth_encoded_msg = eth_account.messages.encode_defunct(text=json.dumps(payload))
        eth_sig_obj = content["sig"]

        if eth_account.Account.recover_message(eth_encoded_msg, signature=eth_sig_obj) == eth_pk:
            result = True  # Should only be true if signature validates
            return jsonify(result)

    # Algorand
    if content["payload"]["platform"] == 'Algorand':
        payload = content["payload"]
        algo_pk = payload["sender_pk"]
        algo_sig_str = content["sig"]

        if algosdk.util.verify_bytes(json.dumps(payload).encode('utf-8'), algo_sig_str, algo_pk):
            result = True  # Should only be true if signature validates
            return jsonify(result)
    
    result = False  # Should only be true if signature validates
    return jsonify(result)

# Helper method to log messages in the Log table
def log_message(d):
    try:
        log = Log(message=json.dumps(d))
        g.session.add(log)
        g.session.commit()
    except Exception as e:
        print(f"Error logging message: {str(e)}")

# Trade endpoint
@app.route('/trade', methods=['POST'])
def trade():
    if request.method == "POST":
        content = request.get_json(silent=True)
        print(f"content = {json.dumps(content)}")
        columns = ["sender_pk", "receiver_pk", "buy_currency", "sell_currency", "buy_amount", "sell_amount", "platform"]
        fields = ["sig", "payload"]
        error = False
        for field in fields:
            if not field in content:
                print(f"{field} not received by Trade")
                print(json.dumps(content))
                log_message(content)
                return jsonify(False)

        error = False
        if "payload" in content:
            payload = content["payload"]
            for column in columns:
                if column not in payload:
                    print(f"{column} not received by Trade")
                    error = True

        if error:
            print(json.dumps(content))
            log_message(content)
            return jsonify(False)

        try:
            sender_pk = payload['sender_pk']
            platform = payload['platform']

            if sender_pk and platform in ['Algorand', 'Ethereum']:
                sig = content['sig']

                # Check if the signature is valid using the /verify endpoint
                verify_payload = {
                    "sig": sig,
                    "payload": payload
                }
                response = requests.post("http://localhost:5002/verify", json=verify_payload)

                if response.status_code == 200 and response.json():
                    # If the signature is valid, insert the order into the Order table
                    order = Order(
                        sender_pk=sender_pk,
                        receiver_pk=payload['receiver_pk'],
                        buy_currency=payload['buy_currency'],
                        sell_currency=payload['sell_currency'],
                        buy_amount=payload['buy_amount'],
                        sell_amount=payload['sell_amount'],
                        signature=sig
                    )

                    g.session.add(order)
                    g.session.commit()
                    return jsonify(True)
                else:
                    log_message(payload)
                    return jsonify(False)
            else:
                log_message(payload)
                return jsonify(False)
        except Exception as e:
            print(f"Error processing trade request: {str(e)}")
            return jsonify(False)
