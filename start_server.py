from util import *
import atexit
import babydes as bd
import diffiehellman as dh
import hash as hsh
import numpy as np
import os
import rsa
import sys
import time

attributions = """
=============================================================================================
  _____           _           _             _   _        _ _           _   _
 |  __ \         (_)         | |       /\  | | | |      (_) |         | | (_)
 | |__) | __ ___  _  ___  ___| |_     /  \ | |_| |_ _ __ _| |__  _   _| |_ _  ___  _ __  ___
 |  ___/ '__/ _ \| |/ _ \/ __| __|   / /\ \| __| __| '__| | '_ \| | | | __| |/ _ \| '_ \/ __|
 | |   | | | (_) | |  __/ (__| |_   / ____ \ |_| |_| |  | | |_) | |_| | |_| | (_) | | | \__ \
 |_|   |_|  \___/| |\___|\___|\__| /_/    \_\__|\__|_|  |_|_.__/ \__,_|\__|_|\___/|_| |_|___/
                _/ |
               |__/
=============================================================================================
Front-End and Messaging Protocol:                                             Rishika Mohanta
Diffie Hellman :                                                               Ramya Narayanan
RSA :                                                                         Samarendra Pani
Client Authentication:                                                    Rohit Sahasrabuddhe
BabyDES:                                                                     All Team Members
=============================================================================================
"""
def exit_handler():
    if not os.path.exists('hacker.log'):
        os.remove('hacker.log')
    print(attributions)

atexit.register(exit_handler)

## Setup Messaging Protocol ##
# Listener #
def listen():
    keep_listening = True
    while keep_listening:
        if os.path.exists(f"{IP}/port{port}/client2server.message"):
            with open(f"{IP}/port{port}/client2server.message", "r") as f:
                message = f.readline()
            keep_listening = False
            os.remove(f"{IP}/port{port}/client2server.message")
        time.sleep(0.5)
    print(f"Message Received: '{message}'")
    message = decompress(message)
    if showcompression:
        print(f"Decompressed Message: '{message}'")
    if bDESkey is not None:
        message = bd.bDES_decryption(message,bDESkey)
        print(f"Decrypted Message: {message}")
    return message
# Messenger #
def reply(message):
    message = str(message)
    busy = True
    if bDESkey is not None:
        print(f"Encrypting reply: '{message}'...")
        message = bd.bDES_encryption(message,bDESkey)
    if showcompression:
        print(f"Compressing reply: '{message}'...")
    message = compress(message)
    print(f"Sending Reply: '{message}'...",end='')
    t0= time.time()
    while busy:
        if not os.path.exists(f"{IP}/port{port}/server2client.message"):
            with open(f"{IP}/port{port}/server2client.message", "w") as f:
                f.write(message)
            busy = False
            time.sleep(1)
        if time.time()-t0 > 60:
            print("Sending Failed. Client Unresponsive.")
            return
    hackerlog(message)
    print("Sent")

## Set up Client System Structure ##

digits =4
bDESkey = None

password = "12345678"
keyexchanged = False
authenticated = False
showcompression = True

# Default user@server port to connect #
if len(sys.argv)==2:
    IP = sys.argv[1]
    port = "22"
    user = "root"
elif len(sys.argv)==3:
    IP = sys.argv[1]
    port = sys.argv[2]
    user = "root"
elif len(sys.argv)==4:
    IP = sys.argv[1]
    port = sys.argv[2]
    user = sys.argv[3]
else:
    IP = "192.168.0.1"
    port = "22"
    user = "root"

# Setup the Server Structure
if not os.path.exists(f'{IP}'):
    os.makedirs(f'{IP}/port{port}')
    os.makedirs(f'{IP}/{user}')
    os.makedirs(f'{IP}/{user}/.ssh/')
else:
    if not os.path.exists(f'{IP}/port{port}'):
        os.makedirs(f'{IP}/port{port}')
    if not os.path.exists(f'{IP}/{user}'):
        os.makedirs(f'{IP}/{user}/.ssh/')

# Set up SSH data #
if not os.path.exists(f'{IP}/{user}/.ssh/authorized_keys'):
    f = open(f"{IP}/{user}/.ssh/authorized_keys", "w")
    f.close()

# Set up RSA keypairs for the first time #
if not (os.path.exists(f'{IP}/{user}/.ssh/id_rsa.pub') and os.path.exists(f'{IP}/{user}/.ssh/id_rsa')):
    print("Generating server RSA Keys...", end="")
    pub,pri = rsa.generate_RSA_keys(digits)
    with open(f"{IP}/{user}/.ssh/id_rsa", "w") as f:
        f.write(f"{pri[0]}:{pri[1]}")
    with open(f"{IP}/{user}/.ssh/id_rsa.pub", "w") as f:
        f.write(f"{pub[0]}:{pub[1]}")
    print("Generated")

# Clean up the channel for communication
for i in os.listdir(f'{IP}/port{port}'):
    os.remove(f'{IP}/port{port}/{i}')

## Initialize the Server ##
startmessage = f"""
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 __          __  _                            _          ____        _            _____ _____ _    _
 \ \        / / | |                          | |        |  _ \      | |          / ____/ ____| |  | |
  \ \  /\  / /__| | ___ ___  _ __ ___   ___  | |_ ___   | |_) | __ _| |__  _   _| (___| (___ | |__| |
   \ \/  \/ / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \  |  _ < / _` | '_ \| | | |\___ \\___ \ |  __  |
    \  /\  /  __/ | (_| (_) | | | | | |  __/ | || (_) | | |_) | (_| | |_) | |_| |____) |___) | |  | |
     \/  \/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/  |____/ \__,_|_.__/ \__, |_____/_____/|_|  |_|
                                                                            __/ |
                                                                           |___/
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
BabySSH Server Started on IP {IP}. Listening to Port {port}.
KEYEX_ALGORITHM:DIFFIEHELLMAN
PUBKEYENC_ALGORITHM:RSA
SYMKEYENC_ALGORITHM:BABYDES
HASH_ALGORITHM:KNUTHVARIANTDIVISION
COMPRESSION:ZLIB""".format(IP=IP,port=port)
print(startmessage)

while True:
    message = listen()
    if keyexchanged:
        showcompression = False
    # respond to public key request #
    if message == "request:publickey":
        with open(f'{IP}/{user}/.ssh/id_rsa.pub', "r") as f:
            pubkey_server = f.read()
        reply(pubkey_server)

    # respond to key exchange request #
    elif message == "init:keyexchange":
        p = dh.getSafePrime(digits)
        g = dh.getPrimitiveRoot(p)
        privatekey_server = np.random.randint(2,high=p-1)
        pubm_server = dh.genPublicMessage(p,g,privatekey_server)
        reply(f"{p}:{g}:{pubm_server}")
        pubm_client = int(listen())
        sharedkey = dh.genSharedKey(p,pubm_client,privatekey_server)
        np.random.seed(sharedkey)
        bDESkey = list(np.random.choice([False,True],size=9))
        np.random.seed()
        keyexchanged = True
        print(f"Key exchanged. Shared bDES Key is: {bool2str(bDESkey)}. Channel is now secure.")

    # respond to authentication request #
    elif message[:13] == "authenticate:" and keyexchanged:
        pubkey_client = message[13:]
        with open(f'{IP}/{user}/.ssh/authorized_keys', "r") as f:
            authorized_keys = f.readlines()
        if not (pubkey_client in authorized_keys):
            reply(f"Key is not authorized")
            if password == listen():
                with open(f'{IP}/{user}/.ssh/authorized_keys', "a") as f:
                    f.write(pubkey_client)
            else:
                reply("Incorrect Password")
        reply("Key is authorized")
        pubkey_client = pubkey_client.split(":")
        pubkey_client = int(pubkey_client[0]),int(pubkey_client[1])

        authentication_code = np.random.randint(1000, 9999)
        authentication_code_enc = rsa.RSA_encrypt(authentication_code, pubkey_client)
        reply(f"{authentication_code_enc}")
        authentication_code += sum([int(bDESkey[i])*2**i for i in range(len(bDESkey))])
        hashed_code = hsh.hash_it(authentication_code)
        if str(hashed_code) == listen():
            reply("Authentication successful")
            authenticated = True
        else:
            reply("Authentication failed")

    # respond to exit request #
    elif message == "exit":
        bDESkey = None
        keyexchanged = False
        authenticated = False
        showcompression = True
    # respond to general CLI request #
    elif keyexchanged and authenticated:
        with os.popen(message) as process:
            output = process.read()
            if output == "":
                reply("NULL OUTPUT. Possible Error.")
            else:
                reply(output)

    else:
        reply("ERROR. Message not understood.")
