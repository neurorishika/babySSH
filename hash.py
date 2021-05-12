from util import *

def hash_it(x):
    '''
    Utility Function to use a basic hash
    Implemented by Rohit Sahasrabuddhe
    '''
    return (x*(x+3)) % 42023

def MAC(message,sharedkey):
    hashin = str(message)+bool2str(sharedkey)
    hashin = int.from_bytes(hashin.encode("utf-8"),"big")
    return str(hash_it(hashin))
