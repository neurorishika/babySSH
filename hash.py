from util import *

def hash_it(x):
    '''
    Utility Function to use a basic hash
    Implemented by Rohit Sahasrabuddhe
    '''
    if isinstance(x, str):
        x = int.from_bytes(x.encode("utf-8"),"big")
    return (x*(x+3)) % 42023

def MAC(message,sharedkey):
    hashin = str(message)+bool2str(sharedkey)
    return str(hash_it(hashin))
