#!/usr/bin/python3

from algosdk import mnemonic
from algosdk import account
from web3 import Web3
#from ethereum_hd_wallet import EthereumHDWallet
from eth_account import Account


w3 = Web3()
#w3.eth.account.enable_unaudited_hdwallet_features()
#acct,mnemonic_secret = w3.eth.account.create_with_mnemonic()
#print("Mnemonic Secret:", mnemonic_secret)
#Mnemonic Secret: fruit subject silly guitar enjoy tell cat upgrade uniform anxiety laugh melt

# Define the mnemonic phrase
eth_mnemonic_phrase = "fruit subject silly guitar enjoy tell cat upgrade uniform anxiety laugh melt"

eth_acct = w3.eth.account.from_mnemonic(eth_mnemonic_secret)
eth_pk = acct._address
eth_sk = acct._private_key

################
# Generate or store the mnemonic for the account
algo_mnemonic_secret = "eternal chapter thought smile rookie car glue catch height tool auto flame car mention broom print suffer secret glue disorder knee swallow aspect ability delay"
#Private key: bJrJwcvsXYl8DCRVKzkfhCURLJrDqsWm8Mf2wz1sryEg6ahD4y6K+e6uRqnhuo+Yc73TppN+imaWrsMKutC76A==
#Address: EDU2QQ7DF2FPT3VOI2U6DOUPTBZ33U5GSN7IUZUWV3BQVOWQXPUL7YYHQA

# Convert the mnemonic to a private key and public key
algo_sk = mnemonic.to_private_key(algo_mnemonic_secret)
algo_pk = mnemonic.to_public_key(algo_mnemonic_secret)


