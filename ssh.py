import numpy as np
import time
import os
import sys

if len(sys.argv)==2:
    IP = sys.argv[1]
    port = "22"
elif len(sys.argv)==3:
    IP = sys.argv[1]
    port = sys.argv[2]
else:
    IP = "192.168.0.1"
    port = "22"


startmessage = f"""
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 __          __  _                            _          ____        _            _____ _____ _    _
 \ \        / / | |                          | |        |  _ \      | |          / ____/ ____| |  | |
  \ \  /\  / /__| | ___ ___  _ __ ___   ___  | |_ ___   | |_) | __ _| |__  _   _| (___| (___ | |__| |
   \ \/  \/ / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \  |  _ < / _` | '_ \| | | |\___ \\___ \|  __  |
    \  /\  /  __/ | (_| (_) | | | | | |  __/ | || (_) | | |_) | (_| | |_) | |_| |____) |___) | |  | |
     \/  \/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/  |____/ \__,_|_.__/ \__, |_____/_____/|_|  |_|
                                                                            __/ |
                                                                           |___/
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
BabySSH Client Started."""
print(startmessage)

if not os.path.exists(f'{IP}'):
    print("Server Doesnt Exist.")
else:
    if not os.path.exists(f'{IP}/port{port}'):
        print("Port not listening.")

print("Connection possible with IP {IP} port {port}.".format(IP=IP,port=port))

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
    return message

def send(message):
    busy = True
    print(f"Sending Message: '{message}'...",end='')
    t0= time.time()
    while busy:
        if not os.path.exists(f"{IP}/port{port}/client2server.message"):
            with open(f"{IP}/port{port}/client2server.message", "w") as f:
                message = f.write(message)
            busy = False
            time.sleep(1)
        if time.time()-t0 > 60:
            print("Sending Failed. Client Unresponsive.")
            return
    print("Sent")

def processboolean():
    query = input("Send Message (y/n)? ")
    if query.lower()[0] == 'y':
        return True
    elif query.lower()[0] == 'n':
        return False
    else:
        return processboolean()

while processboolean():
    message = input("Enter Message: ")
    send(message)
    listen()
