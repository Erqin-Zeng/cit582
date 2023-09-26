from flask import Flask, request, g
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from flask import jsonify
import json
import eth_account
import algosdk
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import load_only
from datetime import datetime
import math
import sys
import traceback

from algosdk import mnemonic
from algosdk import account
from web3 import Web3
#from ethereum_hd_wallet import EthereumHDWallet
from eth_account import Account

# TODO: make sure you implement connect_to_algo, send_tokens_algo, and send_tokens_eth
from send_tokens import connect_to_algo, connect_to_eth, send_tokens_algo, send_tokens_eth

from models import Base, Order, TX
engine = create_engine('sqlite:///orders.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

app = Flask(__name__)

""" Pre-defined methods (do not need to change) """

@app.before_request
def create_session():
    g.session = scoped_session(DBSession)

@app.teardown_appcontext
def shutdown_session(response_or_exc):
    sys.stdout.flush()
    g.session.commit()
    g.session.remove()

def connect_to_blockchains():
    try:
        # If g.acl has not been defined yet, then trying to query it fails
        acl_flag = False
        g.acl
    except AttributeError as ae:
        acl_flag = True
    
    try:
        if acl_flag or not g.acl.status():
            # Define Algorand client for the application
            g.acl = connect_to_algo()
    except Exception as e:
        print("Trying to connect to algorand client again")
        print(traceback.format_exc())
        g.acl = connect_to_algo()
    
    try:
        icl_flag = False
        g.icl
    except AttributeError as ae:
        icl_flag = True
    
    try:
        if icl_flag or not g.icl.health():
            # Define the index client
            g.icl = connect_to_algo(connection_type='indexer')
    except Exception as e:
        print("Trying to connect to algorand indexer client again")
        print(traceback.format_exc())
        g.icl = connect_to_algo(connection_type='indexer')

        
    try:
        w3_flag = False
        g.w3
    except AttributeError as ae:
        w3_flag = True
    
    try:
        if w3_flag or not g.w3.isConnected():
            g.w3 = connect_to_eth()
    except Exception as e:
        print("Trying to connect to web3 again")
        print(traceback.format_exc())
        g.w3 = connect_to_eth()
        
""" End of pre-defined methods """
        
""" Helper Methods (skeleton code for you to implement) """

def log_message(d):
    try:
        log = Log(message=json.dumps(d))
        g.session.add(log)
        g.session.commit()
    except Exception as e:
        print(f"Error logging message: {str(e)}")

def get_algo_keys():
    
    # TODO: Generate or read (using the mnemonic secret) 
    # the algorand public/private keys
    algo_mnemonic_secret = "eternal chapter thought smile rookie car glue catch height tool auto flame car mention broom print suffer secret glue disorder knee swallow aspect ability delay"
    algo_sk = mnemonic.to_private_key(algo_mnemonic_secret)
    algo_pk = mnemonic.to_public_key(algo_mnemonic_secret)
    return algo_sk, algo_pk

def get_eth_keys():
    w3 = Web3()
    
    # TODO: Generate or read (using the mnemonic secret) 
    # the ethereum public/private keys
    eth_mnemonic_secret = "fruit subject silly guitar enjoy tell cat upgrade uniform anxiety laugh melt"
    eth_acct = w3.eth.account.from_mnemonic(eth_mnemonic_secret)
    eth_pk = acct._address
    eth_sk = acct._private_key
    return eth_sk, eth_pk


def fill_order(order, txes=[]):
    # TODO: 
    # Match orders (same as Exchange Server II)
    # Validate the order has a payment to back it (make sure the counterparty also made a payment)
    for tx in txes:
        if tx['platform'] == order.sell_currency and tx['receiver_pk'] == order.sender_pk and tx['sell_amount']==order.sell_amount:
            tx2=tx.counterparty
            order2=order.counterparty
            if tx2['platform'] == order2.sell_currency and tx2['receiver_pk'] == order2.sender_pk and tx2['sell_amount']==order2.sell_amount:
                return True
            print("Error: Counter order is not backed by a payment.")
                return False                
    print("Error: Order is not backed by a payment.")
    return False

    # Make sure that you end up executing all resulting transactions!

    
    pass
  
def execute_txes(txes):
    if txes is None:
        return True
    if len(txes) == 0:
        return True
    print( f"Trying to execute {len(txes)} transactions" )
    print( f"IDs = {[tx['order_id'] for tx in txes]}" )
    eth_sk, eth_pk = get_eth_keys()
    algo_sk, algo_pk = get_algo_keys()
    
    if not all( tx['platform'] in ["Algorand","Ethereum"] for tx in txes ):
        print( "Error: execute_txes got an invalid platform!" )
        print( tx['platform'] for tx in txes )

    algo_txes = [tx for tx in txes if tx['platform'] == "Algorand" ]
    eth_txes = [tx for tx in txes if tx['platform'] == "Ethereum" ]

    # TODO: 
    #   1. Send tokens on the Algorand and eth testnets, appropriately
    #      We've provided the send_tokens_algo and send_tokens_eth skeleton methods in send_tokens.py
    algo_tx_ids = send_tokens_algo(g.acl, algo_sk, algo_txes)
    eth_tx_ids = send_tokens_eth(g.w3, eth_sk, eth_txes)
    
    #   2. Add all transactions to the TX table
    try:
        for algo_tx_id in algo_tx_ids:
            algo_tx = TX(
                platform="Algorand",
                receiver_pk=algo_tx['receiver_pk'],
                order_id=algo_tx['order_id'],
                tx_id=algo_tx_id
            )
            g.session.add(algo_tx)

        for eth_tx_id in eth_tx_ids:
            eth_tx = TX(
                platform="Ethereum",
                receiver_pk=eth_tx['receiver_pk'],
                order_id=eth_tx['order_id'],
                tx_id=eth_tx_id
            )
            g.session.add(eth_tx)

        g.session.commit()
        return True
    except Exception as e:
        print(f"Error adding transactions to TX table: {str(e)}")
        return False
    pass

""" End of Helper methods"""
  
@app.route('/address', methods=['POST'])
def address():
    if request.method == "POST":
        content = request.get_json(silent=True)
        if 'platform' not in content.keys():
            print( f"Error: no platform provided" )
            return jsonify( "Error: no platform provided" )
        if not content['platform'] in ["Ethereum", "Algorand"]:
            print( f"Error: {content['platform']} is an invalid platform" )
            return jsonify( f"Error: invalid platform provided: {content['platform']}"  )
        
        if content['platform'] == "Ethereum":
            #Your code here
            eth_sk, eth_pk = get_eth_keys()
            return jsonify( eth_pk )
        if content['platform'] == "Algorand":
            #Your code here
            algo_sk, algo_pk = get_algo_keys()
            return jsonify( algo_pk )

@app.route('/trade', methods=['POST'])
def trade():
    print( "In trade", file=sys.stderr )
    connect_to_blockchains()
    get_keys()
    if request.method == "POST":
        content = request.get_json(silent=True)
        columns = [ "buy_currency", "sell_currency", "buy_amount", "sell_amount", "platform", "tx_id", "receiver_pk"]
        fields = [ "sig", "payload" ]
        error = False
        for field in fields:
            if not field in content.keys():
                print( f"{field} not received by Trade" )
                error = True
        if error:
            print( json.dumps(content) )
            return jsonify( False )
        
        error = False
        for column in columns:
            if not column in content['payload'].keys():
                print( f"{column} not received by Trade" )
                error = True
        if error:
            print( json.dumps(content) )
            return jsonify( False )
        
        # Your code here
        
        # 1. Check the signature
        
        # 2. Add the order to the table
        
        # 3a. Check if the order is backed by a transaction equal to the sell_amount (this is new)

        # 3b. Fill the order (as in Exchange Server II) if the order is valid
        
        # 4. Execute the transactions
        
        # If all goes well, return jsonify(True). else return jsonify(False)
        return jsonify(True)

@app.route('/order_book')
def order_book():
    fields = [ "buy_currency", "sell_currency", "buy_amount", "sell_amount", "signature", "tx_id", "receiver_pk", "sender_pk" ]
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
                "signature": order.signature,
                "tx_id": order.tx_id #add the tx_id field
            }
            order_list.append(order_dict)

        # Create a result dictionary 
        result = {"data": order_list}

        # Return the result as JSON
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(port='5002')
