from math import gcd
import numpy as np
from util import *

def getSafePrime(digits):
    '''
    To get the a random safe prime of the form p = 2q+1 where q is also a prime
    Implemented by Rishika Mohanta
    '''
    while True:
        p = generate_prime(digits)
        if MillerRabin_test(int((p-1)/2)):
            print("Generated Safe Prime...",end="")
            return p

def getPrimitiveRoot(p):
    '''
    To get the first primitive root mod n
    Implemented by Rishika Mohanta
    '''
    coprime_set = {num for num in range (1, p) if gcd(num, p) == 1}
    for g in range(1, p):
        generated_set = set(pow(g, powers) % p for powers in range (1, p))
        if coprime_set == generated_set:
            print(f"Generated primitive root modulo p.")
            return g

def genPublicMessage(p,g,privatekey):
    '''
    To generate DH public message
    Implemented by Ramya Narayanan
    '''
    return int(pow(g,privatekey,p))

def genSharedKey(p,publicmessage,privatekey):
    '''
    To generate DH shared key
    Implemented by Ramya Narayanan
    '''
    return int(pow(publicmessage,privatekey,p))
