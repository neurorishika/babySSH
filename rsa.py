import numpy as np
from util import *

'''
-------------------------------------------------------------------------------------------------------------------------
RSA key generation, encryption and decryption by Samarendra
-------------------------------------------------------------------------------------------------------------------------
'''

def generate_RSA_keys(digits):
    p = generate_prime(digits)
    q = generate_prime(digits)
    n = p*q
    while True:
        e = generate_prime(digits-1)
        if np.gcd(e, (p-1)*(q-1)):
            break
    d = pow(e, -1, (p-1)*(q-1))
    #Returns public key, private key as tuples
    return (n, e), (n, d)

def RSA_encrypt(message, key):
    #key is of form (n, e)
    return pow(message, key[1], key[0])

def RSA_decrypt(message, key):
    #key is of form (n, d)
    return pow(message, key[1], key[0])
