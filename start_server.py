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

if not os.path.exists(f'{IP}'):
    os.makedirs(f'{IP}/port{port}')
elif not os.path.exists(f'{IP}/port{port}'):
        os.makedirs(f'{IP}/port{port}')
else:
    for i in os.listdir(f'{IP}/port{port}'):
        os.remove(f'{IP}/port{port}/{i}')

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
BabySSH Server Started on IP {IP} with port {port}.
Listening to Port {port}...""".format(IP=IP,port=port)
print(startmessage)

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
    return message

def reply(message):
    busy = True
    print(f"Sending Reply: '{message}'...",end='')
    t0= time.time()
    while busy:
        if not os.path.exists(f"{IP}/port{port}/server2client.message"):
            with open(f"{IP}/port{port}/server2client.message", "w") as f:
                message = f.write(message)
            busy = False
            time.sleep(1)
        if time.time()-t0 > 60:
            print("Sending Failed. Client Unresponsive.")
            return
    print("Sent")

while True:
    message = listen()
    if message == "PP very big":
        reply("Nice :)!")
    else:
        reply("What?")
