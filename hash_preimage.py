import hashlib
import os
import random
import string

def hash_preimage(target_string):
    if not all( [x in '01' for x in target_string ] ):
        print( "Input should be a string of bits" )
        return
    nonce = b'\x00'
    #generate first guess
    characters_x = string.ascii_letters + string.digits + string.punctuation
    x = ''.join(random.choice(characters_x) for i in range(20)) # is 20 ok?
    hash_x = hashlib.sha256(x.encode('utf-8')).hexdigest()
    hash_binary_x = bin(int(hash_x, 16))
    x_string = hash_binary_x[len(hash_binary_x) - len(target_string):]

    #continue guessing
    while x_string != target_string:
        characters_x = string.ascii_letters + string.digits + string.punctuation
        x = ''.join(random.choice(characters_x) for i in range(20))  # is 20 ok?
        hash_x = hashlib.sha256(x.encode('utf-8')).hexdigest()
        hash_binary_x = bin(int(hash_x, 16))
        x_string = hash_binary_x[len(hash_binary_x) - len(target_string):]

    nonce = x

    return( nonce )

