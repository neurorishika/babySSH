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
   ______          _           _    ___  _   _        _ _           _   _
   | ___ \        (_)         | |  / _ \| | | |      (_) |         | | (_)
   | |_/ / __ ___  _  ___  ___| |_/ /_\ \ |_| |_ _ __ _| |__  _   _| |_ _  ___  _ __  ___
   |  __/ '__/ _ \| |/ _ \/ __| __|  _  | __| __| '__| | '_ \| | | | __| |/ _ \| '_ \/ __|
   | |  | | | (_) | |  __/ (__| |_| | | | |_| |_| |  | | |_) | |_| | |_| | (_) | | | \__ \
   \_|  |_|  \___/| |\___|\___|\__\_| |_/\__|\__|_|  |_|_.__/ \__,_|\__|_|\___/|_| |_|___/
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
    if os.path.exists('hacker.log'):
        os.remove('hacker.log')
    if os.path.exists('hacker_decompressed.log'):
        os.remove('hacker_decompressed.log')
    print(attributions)

atexit.register(exit_handler)

## Setup Messaging Protocol ##
# Listener #
def listen():

    keep_listening = True
    while keep_listening:
        if os.path.exists(f"{IP}/port{port}/server2client.message"):
            with open(f"{IP}/port{port}/server2client.message", "r") as f:
                message = f.readline()
            keep_listening = False
            os.remove(f"{IP}/port{port}/server2client.message")
        time.sleep(0.5)

    print(f"Message Received: '{message}'")

    message = decompress(message)
    if showcompression:
        print(f"Decompressed Message: '{message}'")

    if bDESkey is not None:
        message = bd.bDES_decryption(message,bDESkey)
        message,mac = message.split("||")
        print(f"Decrypted Message: {message}")
        if hsh.MAC(message,bDESkey) == mac:
            print(f"Message is authentic")
        else:
            print(f"Message is not authentic. You are under attack.")
            quit()

    return message
# Messenger #
def send(message):

    message = str(message)
    if bDESkey is not None:
        message = message+"||"+hsh.MAC(message,bDESkey)
        print(f"Encrypting reply: '{message}'...")
        message = bd.bDES_encryption(message,bDESkey)

    if showcompression:
        print(f"Compressing reply: '{message}'...")

    message = compress(message)
    print(f"Sending Message: '{message}'...",end='')

    t0= time.time()
    busy = True
    while busy:
        if not os.path.exists(f"{IP}/port{port}/client2server.message"):
            with open(f"{IP}/port{port}/client2server.message", "w") as f:
                f.write(message)
            busy = False
            time.sleep(1)
        if time.time()-t0 > 60:
            print("Sending Failed. Client Unresponsive.")
            return

    hackerlog(message)
    print("Sent")

## Set up Client System Structure ##

digits = 4
bDESkey = None
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


if not os.path.exists('client'):
    os.makedirs('client/.ssh/')
if not os.path.exists('client/.ssh/known_hosts'):
    f = open("client/.ssh/known_hosts", "w")
    f.close()

# Set up RSA keypairs for the first time #
if not (os.path.exists(f'client/.ssh/id_rsa.pub') and os.path.exists(f'client/.ssh/id_rsa')):
    print("Generating client RSA Keys...", end="")
    pub,pri = rsa.generate_RSA_keys(digits)
    with open("client/.ssh/id_rsa", "w") as f:
        f.write(f"{pri[0]}:{pri[1]}")
    with open("client/.ssh/id_rsa.pub", "w") as f:
        f.write(f"{pub[0]}:{pub[1]}")
    print("Generated")

## Initialize the Client ##
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
BabySSH Client Started.
KEYEX_ALGORITHM:DIFFIEHELLMAN
PUBKEYENC_ALGORITHM:RSA
SYMKEYENC_ALGORITHM:BABYDES
HASH_ALGORITHM:KNUTHVARIANTDIVISION
COMPRESSION:ZLIB
"""
print(startmessage)

# Ensure the target user/server/port are active #
if not os.path.exists(f'{IP}'):
    print("Server Doesnt Exist.")
else:
    if not os.path.exists(f'{IP}/port{port}'):
        print("Port not listening.")
    if not os.path.exists(f'{IP}/{user}'):
        print("User does not exist.")

## Initialize the Transport Layer ##
# We simplify the Transport layer to allow for only a single set of algorithm that is
# 1. RSA for publickey
# 2. Diffie hellman for Key exchange
# 3. BabyDES for Symmetric Encryption
# 4. Knuth Variant on Division Method for Hash
# 5. Simplified HMAC algorithm

print("Connecting with {user}@{IP}:{port}".format(user=user,IP=IP,port=port))

print("Continue with Server Verification (y/n)?",end="")
processboolean()

print("Querying RSA Public key...")

# send request for public key of the server #
send("request:publickey")
pubkey_server = listen()

# gather known_hosts #
with open('client/.ssh/known_hosts', "r") as f:
    known_hosts = f.readlines()

# check if host in known, if not add to known_hosts #
if f"{IP} {pubkey_server}" in known_hosts:
    print("Host public key matches. Server Verified.")
else:
    print("Server not in known_hosts. Server cannot be verified. Add to known_hosts (y/n)?")
    if processboolean():
        with open('client/.ssh/known_hosts', "a") as f:
            f.write(f"{IP} {pubkey_server}")
    print("Public key added to known_hosts.")

print("Continue with Key Exchange (y/n)?",end="")
processboolean()

# initialize key exchange #
send("init:keyexchange")

# exchange p, g and public message #
p,g,pubm_server = [int(i) for i in listen().split(":")]
privatekey_client = np.random.randint(2,high=p-1)
print("Private key generated.")
pubm_client = dh.genPublicMessage(p,g,privatekey_client)
send(f"{pubm_client}")

# generate shared key using the DH key as the seed for the pseudorandom number generator #
sharedkey = dh.genSharedKey(p,pubm_server,privatekey_client)
print("Shared key generated.")
np.random.seed(sharedkey)
bDESkey = list(np.random.choice([False,True],size=9))
np.random.seed()

print(f"Key exchanged. Shared bDES Key is: {bool2str(bDESkey)}. Channel is now secure.")

showcompression = False

## Initialize the Authentication Layer ##
print("Continue with User Authentication (y/n)?",end="")
processboolean()

# get client public key #
with open('client/.ssh/id_rsa.pub', "r") as f:
    pubkey_client = f.read()

# send authentication request #
send(f"authenticate:{pubkey_client}")

# check if the client key is authorised, otherwise add to authorized with password #
reply = listen()
if "Key is not authorized" == reply:
    password = input(f"Insert {user} password to authorize the key: ")
    send(password)
    reply = listen()
    if reply == "Incorrect Password":
        print("Authentication Failed. Closing BabySSH client.")
        quit()

# start authencation protocol using RSA and Hash#
if "Key is authorized" == reply:
    authentication_code = int(listen())
    print("Authentication message received.")

    with open('client/.ssh/id_rsa', "r") as f:
        prikey_client = f.read()
    prikey_client = prikey_client.split(":")
    prikey_client = int(prikey_client[0]),int(prikey_client[1])

    authentication_code = rsa.RSA_decrypt(authentication_code,prikey_client)
    print("Authentication message decrypted.")

    authentication_code += sum([int(bDESkey[i])*2**i for i in range(len(bDESkey))])
    hashed_code = hsh.hash_it(authentication_code)
    print("Hash generated.")

    send(hashed_code)
    reply = listen()
    if reply == "Authentication failed":
        print("Authentication failed. Closing BabySSH client.")
        quit()
    elif reply == "Authentication successful":
        print(f"Authenticated {user}. Welcome to {IP}!")
    else:
        print("Authentication failed. Closing BabySSH client.")
        quit()

# Start remote connection pipe #
while True:
    message = input(f"{user}@{IP}:")
    if message == "exit":
        print("Closing BabySSH client.")
        send("exit")
        quit()
    if message == "":
        continue
    send(message)
    listen()
