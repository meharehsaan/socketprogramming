# https://github.com/meharehsaan
# UDP socket  sender(server) file
# Importing modules
import socket
import time
import random
import sys
# Defining host and port AND creating scoket
shost = 'localhost'
sport = 12345
bfsize = 1024
# Socket and binding
sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sender.bind((shost, sport))
print("Socket snd created successfully")

# Rcving loss %age from rcver
msg , raddress = sender.recvfrom(bfsize)
perloss = int(msg.decode("utf-8"))

def stopAndWait():
    global raddress
    count = 0            # For acknowledgement count
    file = open("DataSent.txt", "r")
    fdata = file.read()
    # msg = "Hello"
    # Msg will be sent in single single alphabets
    for data in fdata:
        rand = random.randint(0, 99)
        print(f"Random number : {rand} and Loss %age {perloss}")
        if (rand < perloss):
            sdata = data.encode("utf-8")
            # start = time.time()
            sender.sendto(sdata, raddress)
        else:
            print("Random loss error, Again sending lost data...")
            msg = "error"
            edata = msg.encode("utf-8")
            sender.sendto(edata, raddress)
            time.sleep(0.4)
            sdata = data.encode("utf-8")
            sender.sendto(sdata, raddress)
        msg1 , raddress = sender.recvfrom(bfsize)
        ack = msg1.decode("utf-8")
        # ACK check
        if(ack == "ACK"):
            count = count+1
            print(f"Got {count} ACK successfully. Now futher sending...")
        else:
            print("!error no ACK received, Retransmitting data packet...")
            msg = "error"
            edata = msg.encode("utf-8")
            sender.sendto(edata, raddress)
            time.sleep(0.4)
            sdata = data.encode("utf-8")
            sender.sendto(sdata, raddress)

    # Breaked loop
    print("Data extracted and sent all")
    msg = "ok"                  # Delivering a data end msg to receiver
    data = msg.encode("utf-8")
    sender.sendto(data, raddress)

# Welcome
print("Welcome to the world of sockets where we communicate using ports")
print(f"Loss percentage receiver thinks :: {perloss}")
print("Recever IP and Port :: " , raddress)

# Calling functions for appropiate use of socket
stopAndWait()
print("Shutdowned the Server")