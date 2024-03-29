#!/usr/bin/python3

from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk import transaction
from algosdk import account, encoding

# Generate or store the mnemonic for the account
mnemonic_secret = "eternal chapter thought smile rookie car glue catch height tool auto flame car mention broom print suffer secret glue disorder knee swallow aspect ability delay"
#Private key: bJrJwcvsXYl8DCRVKzkfhCURLJrDqsWm8Mf2wz1sryEg6ahD4y6K+e6uRqnhuo+Yc73TppN+imaWrsMKutC76A==
#Address: EDU2QQ7DF2FPT3VOI2U6DOUPTBZ33U5GSN7IUZUWV3BQVOWQXPUL7YYHQA

# Convert the mnemonic to a private key and public key
sk = mnemonic.to_private_key(mnemonic_secret)
sender_pk = mnemonic.to_public_key(mnemonic_secret)

#Connect to Algorand node maintained by PureStake
algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "B3SU4KcVKi94Jap2VXkK83xx38bsv95K5UZm2lab"
#algod_token = 'IwMysN3FSZ8zGVaQnoUIJ9RXolbQ5nRY62JRqF2H'
headers = {
   "X-API-Key": algod_token,
}

acl = algod.AlgodClient(algod_token, algod_address, headers)
min_balance = 100000 #https://developer.algorand.org/docs/features/accounts/#minimum-balance

def send_tokens( receiver_pk, tx_amount ):
    params = acl.suggested_params()
    gen_hash = params.gh
    first_valid_round = params.first
    tx_fee = params.min_fee
    last_valid_round = params.last

    #Your code here

    # Create the transaction
    txn = transaction.PaymentTxn(
        sender=sender_pk,
        #sp=params,
        receiver=receiver_pk,
        amt=tx_amount,
        gh=gen_hash, #was gen=
        first=first_valid_round,
        last=last_valid_round,
        note=b'',
        fee=tx_fee,
    )

    #Sign the transaction
    stxn = txn.sign(sk) 

    #Send the transaction
    txid = acl.send_transaction(stxn)

    return sender_pk, txid

# Function from Algorand Inc.
def wait_for_confirmation(client, txid):
    """
    Utility function to wait until the transaction is
    confirmed before proceeding.
    """
    last_round = client.status().get('last-round')
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        print("Waiting for confirmation")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print("Transaction {} confirmed in round {}.".format(txid, txinfo.get('confirmed-round')))
    return txinfo


'''# generate an account
sk, sender_pk = account.generate_account()
print("Private key:", sk)
print("Address:", sender_pk)

# check if the address is valid
if encoding.is_valid_address(sender_pk):
    print("The address is valid!")
else:
    print("The address is invalid.")

# Convert the private key to a mnemonic (25 words)
mnemonic_phrase = mnemonic.from_private_key(sk)
print("Generated 25-Word Mnemonic:", mnemonic_phrase)'''
