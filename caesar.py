def encrypt(key,plaintext):
    ciphertext=""
    #YOUR CODE HERE
    for element in plaintext:
        letter_order = ord(element) - 65
        ciphertext = ciphertext + chr((letter_order+(key%26))%26+65)
    return ciphertext

def decrypt(key,ciphertext):
    plaintext=""
    #YOUR CODE HERE
    for element in ciphertext:
        letter_order = ord(element) - 65
        plaintext = plaintext + chr((letter_order-(key%26))%26+65)
    return plaintext
