from flask import Flask, request, g
from flask_restful import Api, Resource
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, JSON, ForeignKey
from sqlalchemy.orm import sessionmaker, scoped_session
from eth_account.messages import encode_defunct
import json
import eth_account
import algosdk
from models import Base, Order, Log

app = Flask(__name__)
api = Api(app)
app.url_map.strict_slashes = False

# Create an SQLite database engine and bind it to the SQLAlchemy metadata
engine = create_engine('sqlite:///orders.db')
Base.metadata.bind = engine

# Create a session maker for database interactions
DBSession = sessionmaker(bind=engine)

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
class Trade(Resource):
    def post(self):
        try:
            content = request.get_json()
            payload = content.get('payload')
            sig = content.get('sig')

            if payload and sig:
                sender_pk = payload.get('sender_pk')
                platform = payload.get('platform')

                if sender_pk and platform in ['Algorand', 'Ethereum']:
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
                        sender_pk=payload['sender_pk'],
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
                return jsonify(False)
        except Exception as e:
            print(f"Error processing trade request: {str(e)}")
            return jsonify(False)

# Order book endpoint
class OrderBook(Resource):
    def get(self):
        try:
            orders = g.session.query(Order).all()
            order_list = []
            for order in orders:
                order_dict = {
                    'sender_pk': order.sender_pk,
                    'receiver_pk': order.receiver_pk,
                    'buy_currency': order.buy_currency,
                    'sell_currency': order.sell_currency,
                    'buy_amount': order.buy_amount,
                    'sell_amount': order.sell_amount,
                    'signature': order.signature
                }
                order_list.append(order_dict)

            return jsonify({'data': order_list})
        except Exception as e:
            print(f"Error fetching order book: {str(e)}")
            return jsonify({'data': []})

api.add_resource(Trade, '/trade')
api.add_resource(OrderBook, '/order_book')

if __name__ == '__main__':
    app.run(port='5002')
