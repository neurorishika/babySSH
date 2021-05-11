import numpy as np
import zlib
import binascii

def compress(message,level=-1):
    '''
    Utility Function to compress using zlib
    Implemented by Rishika Mohanta
    '''
    return binascii.hexlify(zlib.compress(message.encode('utf-8'),level)).decode('utf-8')

def decompress(message,level=-1):
    '''
    Utility Function to decompress using zlib
    Implemented by Rishika Mohanta
    '''
    return zlib.decompress(binascii.unhexlify(message.encode('utf-8'))).decode('utf-8')

def hackerlog(message):
    '''
    Utility Function to log what an hacker would see
    Implemented by Rishika Mohanta
    '''
    with open("hacker.log","a") as f:
        f.write(message+"\n")
    with open("hacker_decompressed.log","a") as f:
        f.write(decompress(message)+"\n")

def processboolean():
    '''
    Utility Function to respond to y/n answers
    Implemented by Rishika Mohanta
    '''
    query = input()
    if len(query) == 0:
        return processboolean()
    if query.lower()[0] == 'y':
        return True
    elif query.lower()[0] == 'n':
        return False
    else:
        return processboolean()


def str2bool(x):
    '''
    Utility Function to convert a binary string to a boolean list
    Implemented by Rishika Mohanta
    '''
    return [bool(int(i)) for i in list(x)]

def bool2str(x):
    '''
    Utility Function to convert a boolean list to a binary string
    Implemented by Rishika Mohanta
    '''
    return "".join([str(int(i)) for i in x])

def text2binary(text, encoding='utf-8', errors='surrogatepass'):
    '''
    Utility Function to convert a Unicode message to a binary string
    Implemented by Rishika Mohanta
    '''
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def binary2text(bits, encoding='utf-8', errors='surrogatepass'):
    '''
    Utility Function to convert a binary string to a Unicode message
    Implemented by Rishika Mohanta
    '''
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

def MillerRabin_test(n):
    '''
    Utility Function to check Primality using Miller Rabin Test.
    Implemented by Samarendra Pani
    '''
    maxDivisionsByTwo = 0
    ec = n-1
    while ec % 2 == 0:
        ec >>= 1
        maxDivisionsByTwo += 1
    assert(2**maxDivisionsByTwo * ec == n-1)
    def trialComposite(round_tester):
        if pow(round_tester, ec, n) == 1:
            return False
        for i in range(maxDivisionsByTwo):
            if pow(round_tester, 2**i * ec, n) == n-1:
                return False
        return True
    numberOfRabinTrials = 20
    for i in range(numberOfRabinTrials):
        round_tester = np.random.randint(2, n)
        if trialComposite(round_tester):
            return False
    return True

def generate_prime(digits):
    '''
    Utility Function to generate prime number with a given number of digits
    Implemented by Samarendra Pani
    '''
    #list of low pre-generated primes
    first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349]
    while True:
        to_continue = False
        n = np.random.randint(low=10**(digits-1), high=10**digits)
        #Checking divisibility with pre-generated prime list
        for divisor in first_primes_list:
            if n % divisor == 0 and divisor**2 <= n:
                to_continue = True
                break
        if to_continue:
            continue
        #Checking Primality with Miller-Rabin test with 20 iterations
        if MillerRabin_test(n):
            break
    return n
