
# https://github.com/meharehsaan
# UDP socket client(receiver) file
# Importing modules
import socket
import time
import random

# Defining host and port AND creating socket
rhost = 'localhost'
rport = 11122
bfsize = 20
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Socket rcv created successfully")

# Address where we want communication
saddress = ('localhost', 12345)

# Sending loss %age variable to compare with Random value in sender
data = int(input("Enter loss percentage : "))  # Integer input to string
while(True):
    if (data < 0 or data > 99):
        print("Plz Enter a number bTW 0, 99")
        data = int(input("Enter loss percentage : "))
    else:
        break
data = str(data)
perloss = data.encode("utf-8")
client.sendto(perloss, saddress)            


def stopAndWait():
    count = 1           # For acknowledgement count
    ecount = 0          # For loss packet count
    fullmsg = ""        # For full msg printing
    # Msg will be received in single single alphabets
    while(True):

        start = time.time()
        data, saddress = client.recvfrom(bfsize)
        msg = data.decode("utf-8")

        # randoms checks to prevent data loss
        if (msg == "ok"):
            print("Received all data from sender")
            break
        if (msg == "error"):
            data, saddress = client.recvfrom(bfsize)
            msg = data.decode("utf-8")
            ecount = ecount + 1
        if (msg != "ok"):
            fullmsg = fullmsg+msg

        # Sending acknowlegdement to sender of received data
        if(str(msg) != ""):
            msg = "ACK"
            data = msg.encode("utf-8")
            client.sendto(data , saddress)
            # time.sleep(1)
            end = time.time()
            print(f"Acknowledgement sent successfully : {count}")
            count = count+1
        else:
            print("ACK didnot sent successfully !error")

    elapsed = start - end
    # print(f"Sender :: {fullmsg}\n")
    file = open("DataReceived.txt", "w")
    file.write(fullmsg)
    file.close()
    
    # stats
    print(f"Total Data packets received {count - ecount}")
    print(f"Total Data packets lost {ecount}")
    print(f"Time taken in transfer {elapsed}")


print("Welcome to the world of sockets where we communicate using ports")

stopAndWait()

print("Receiver shutdowned")