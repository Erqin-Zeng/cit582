from flask import Flask, request, g
from flask_restful import Api, Resource
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, JSON, ForeignKey
from sqlalchemy.orm import sessionmaker, scoped_session
from eth_account.messages import encode_defunct
import json
import eth_account
import algosdk

from models import Base, Order, Log
engine = create_engine('sqlite:///orders.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

app = Flask(__name__)

#api = Api(app)
#app.url_map.strict_slashes = False

# These decorators allow you to use g.session to access the database inside the request code
@app.before_request
def create_session():
    g.session = scoped_session(DBSession)

@app.teardown_appcontext
def shutdown_session(response_or_exc):
    g.session.commit()
    g.session.remove()

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
            if field not in content:
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

                # Check if the signature is valid
                if platform == 'Algorand':
                    algo_sig_str = sig
                    if not algosdk.util.verify_bytes(json.dumps(payload).encode('utf-8'), algo_sig_str, sender_pk):
                        log_message(payload)
                        return jsonify(False)

                elif platform == 'Ethereum':
                    eth_sig_obj = sig
                    eth_encoded_msg = encode_defunct(text=json.dumps(payload))
                    if sender_pk != eth_account.Account.recover_message(eth_encoded_msg, signature=eth_sig_obj):
                        log_message(payload)
                        return jsonify(False)

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
        except Exception as e:
            print(f"Error processing trade request: {str(e)}")
            return jsonify(False)


# Order book endpoint
@app.route('/order_book')
def order_book():
    try:
        # Your code here
        # Note that you can access the database session using g.session
        orders = g.session.query(Order).all()
        order_list = []

        for order in orders:
            order_dict = {
                "sender_pk": order.sender_pk,
                "receiver_pk": order.receiver_pk,
                "buy_currency": order.buy_currency,
                "sell_currency": order.sell_currency,
                "buy_amount": order.buy_amount,
                "sell_amount": order.sell_amount,
                "signature": order.signature
            }
            order_list.append(order_dict)

        # Create a result dictionary 
        result = {"data": order_list}

        # Return the result as JSON
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})


#api.add_resource(Trade, '/trade')
#api.add_resource(OrderBook, '/order_book')

#if __name__ == '__main__':
    #app.run(port='5002')
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002)

