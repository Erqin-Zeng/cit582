import hashlib
import os
import random
import string


def hash_collision(k):
    if not isinstance(k, int):
        print("hash_collision expects an integer")
        return (b'\x00', b'\x00')
    if k < 0:
        print("Specify a positive number of bits")
        return (b'\x00', b'\x00')

    # Collision finding code goes here
    if k >= 256:
        print("Specify a positive number smaller than 256")
        return (b'\x00', b'\x00')


    # generate random x
    characters_x = string.ascii_letters + string.digits + string.punctuation
    x = ''.join(random.choice(characters_x) for i in range(20)) # is 20 ok?
    hash_x = hashlib.sha256(x.encode('utf-8')).hexdigest()
    hash_binary_x = bin(int(hash_x, 16))
    hash_key = hash_binary_x[len(hash_binary_x) - k:]

    #generate random y
    characters_y = string.ascii_letters + string.digits + string.punctuation
    y = ''.join(random.choice(characters_y) for i in range(20))  # is 20 ok?
    hash_y = hashlib.sha256(y.encode('utf-8')).hexdigest()
    hash_binary_y = bin(int(hash_y, 16))
    hash_key_y = hash_binary_y[len(hash_binary_y) - k:]

    while hash_key_y != hash_key and x!=y:
        characters_y = string.ascii_letters + string.digits + string.punctuation
        y = ''.join(random.choice(characters_y) for i in range(20)) # is 20 ok?
        hash_y = hashlib.sha256(y.encode('utf-8')).hexdigest()
        hash_binary_y = bin(int(hash_y, 16))
        hash_key_y = hash_binary_y[len(hash_binary_y) - k:]
    
    x = x.encode('utf-8')
    y = y.encode('utf-8')
    return (x, y)

