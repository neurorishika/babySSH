import numpy as np
from util import *

'''
Server has list of authorized public key.
Client has public key and private key (unique to client).

Server has to make sure that the client who is in contact is authorized.

Authentication:
---------------
    - Server selects a message.
    - Encrypts with public key.
    - Client decrypts it and adds the session key (generated by Diffie Hellman) and then hashes it.
    - Sends the hash encrypted using the algorithm.
    - Server checks if the hash is correct (since it has the original message and session key).

RSA:
----
Have to make public and private key for client side only.
    - Select two huge prime numbers (?? digits), lets call them p and q. Let n = pq.
    - Select e such that gcd(e, (p-1)(q-1)) = 1
    - Compute d such that de = 1 (mod (p-1)(q-1))
    - Client has (n, e) as public key and (n, d) as private key.
    - Encryption of message m: c = m^e (mod n)
    - Decryption of ciphertext c: m = c^d (mod n)
'''

'''
-------------------------------------------------------------------------------------------------------------------------
Previously Developed BabyDES Algorithm
-------------------------------------------------------------------------------------------------------------------------
'''

# Expander Function

def expander(x):
    '''
    Expander function implemented by Ramya Narayanan
    '''
    x.append(x[2])
    x.append(x[3])
    order = [0, 1, 3, 2, 7, 6, 4, 5]
    x = [x[i] for i in order]
    return x


# S-Box

def s_box(in_list, box_number):
    '''
    S-Box function implemented by Rohit Sahasrabuddhe
    in_list: a list of booleans of length 4 (4-bit)
    box_number: 1 or 2
    '''
    S1 = [ [[True , False, True], [False, True , False], [False, False, True ], [True , True , False], [False, True , True ], [True , False, False], [True , True , True ], [False, False, False]],
           [[False, False, True], [True , False, False], [True , True , False], [False, True , False], [False, False, False], [True , True , True ], [True , False, True ], [False, True , True ]]]

    S2 = [ [[True , False, False], [False, False, False], [True , True , False], [True , False, True], [True , True , True ], [False, False, True ], [False, True , True ], [False, True , False]],
           [[True , False, True ], [False, True , True ], [False, False, False], [True , True , True], [True , True , False], [False, True , False], [False, False, True ], [True , False, False]]]

    box = [S1, S2][box_number-1]

    return box[int(in_list[0])][int(''.join(list(map(lambda x: str(int(x)), in_list[1:]))), 2)]


# Round Function

def round_function(Ri, Ki):
    '''
    Round Function implemented by Rishika Mohanta
    Ri: a list of booleans of length 6 (6-Bit ith round; Right Block)
    Ki: a list of booleans of length 8 (8-bit ith round; Round key)
    '''
    ERi = expander(Ri)
    ERi_Ki = np.logical_xor(ERi,Ki)
    ERi_Ki1,ERi_Ki2 = np.array_split(ERi_Ki,2)
    S1_out = s_box(ERi_Ki1,1)
    S2_out = s_box(ERi_Ki2,2)
    return list(np.concatenate([S1_out,S2_out]))


# Single Round Function

def bDES_round(block_1, block_2, des_key, round_number):
    '''
    Single round of bDES implemented by Samarendra Pani
    block_1: a list of booleans of length 6 (The left block in case of encryption. The right block in case of decryption)
    block_2: a list of booleans of length 6 (The right block in case of encryption. The left block in case of decryption)
    des_key: a list of booleans of length 9 (9 bit DES key)
    round_number: 1,2...N for N bDES (To calculate Key Schedule)
    '''
    tmp = list(np.copy(block_2))
    key_8bit = list(np.roll(des_key, -(round_number-1)))[0:8]   #Key scheduling
    block_2 = round_function(block_2, key_8bit)
    block_2 = list(np.logical_xor(block_1, block_2))
    block_1 = tmp

    return block_1, block_2                                     #Returning the blocks after 1 round of encryption


# Encryption function

def bDES_encryption(plaintext, key):
    '''
    bDES encryption implemented by Samarendra Pani
    plaintext: A list of booleans which represents the given plaintext.
    key: A list of booleans of length 9 (9 bit DES key)
    N: The number of rounds for encrypting a block
    '''

    plaintext += '\0'*((3-len(plaintext)%3)%3)
    plaintext = str2bool(text2binary(plaintext))

    N = 4
    output = []
    for i in range(int(len(plaintext)/12)):
        plaintext_block = plaintext[12*i:12*(i+1)]
        block_1 = plaintext_block[0:6]
        block_2 = plaintext_block[6:12]
        round_number = 1
        while(round_number <= N):
            block_1, block_2 = bDES_round(block_1, block_2, key, round_number)
            round_number += 1
        output.extend(block_1 + block_2)

    return bool2str(output)           #Returing the CIPHERTEXT in binary form


# Decryption function

def bDES_decryption(CIPHERTEXT, key):
    '''
    bDES decryption implemented by Samarendra Pani
    CIPHERTEXT: A list of booleans which represents the generated ciphertext.
    key: A list of booleans of length 9 (9 bit DES key)
    N: The number of rounds for decrypting a block (same as the number of rounds it took for encryption)
    '''
    CIPHERTEXT = str2bool(CIPHERTEXT)
    N = 4
    output = []
    for i in range(int(len(CIPHERTEXT)/12)):
        CIPHERTEXT_block = CIPHERTEXT[12*i:12*(i+1)]
        block_1 = CIPHERTEXT_block[6:12]
        block_2 = CIPHERTEXT_block[0:6]
        round_number = N
        while(round_number >= 1):
            block_1, block_2 = bDES_round(block_1, block_2, key, round_number)
            round_number -= 1
        output.extend(block_2 + block_1)

    message = binary2text(bool2str(output))
    try:
        #Removing the null padding
        message = message[:message.index("\x00")]
    except:
        pass
    return message
