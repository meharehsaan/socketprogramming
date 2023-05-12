# https://github.com/meharehsaan
# UDP socket client(receiver) file
# Importing modules
import socket, time 
import random, sys 
import struct, zlib

# Defining host and port AND creating socket
rhost = 'localhost'
rport = 11122
bfsize = 1024
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("Socket rcv created successfully")

# Server address where we want communication
saddress = ('localhost', 12345)
msg = "hy"
data = msg.encode("utf-8")
client.sendto(data, saddress)
print("Welcome to the world of sockets where we communicate using ports")

def addChecksum(data):
    checksum = zlib.crc32(data)
    return checksum

def filewithheader():
    start = time.time()
    file = open("DataReceived.txt", "wb")
    print("Receiving file...")
    time.sleep(0.5)

    while(True):
        fullpacket , saddress = client.recvfrom(bfsize)
        header = fullpacket[:16]          # extracting header from received buffer
        data = fullpacket[16:]            # extracting data
        checksum1 = addChecksum(data)     # adding checksum to received data

        # unpacking header to extract senderport, receiverport, checksum, length
        header = struct.unpack("!IIII", header)
        checksum = header[3]
        char = file.write(data)  # Counting characters written in file
        # validating checksum
        if(checksum == checksum1): 
            print("Checksum :: Data is error free")
            break
        else:
            print("Checksum :: !error")

    # closing file
    file.close()
    end = time.time()
    elapsed = end - start
    print("File Received Successfully")
    time.sleep(0.5)

    # printing stats
    length = header[2]
    print("Transfer time = ", elapsed)
    print("Length of Received Data: ", length) 

# function calling
filewithheader()