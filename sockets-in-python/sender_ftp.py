# https://github.com/meharehsaan
# UDP socket  sender(server) file
# Importing modules
import socket, time 
import random, sys 
import struct, zlib

# Defining host and port AND creating scoket
shost = 'localhost'
sport = 12345
bfsize = 1024
rport = 11122

# Socket and binding
sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sender.bind((shost, sport))
print("Socket created successfully")

print("Welcome to the world of sockets where we communicate using ports")
msg, raddress = sender.recvfrom(bfsize)
data = msg.decode("utf-8")
print(f"Recever IP and Port :: {raddress}")

def addChecksum(data):
    checksum = zlib.crc32(data)
    return checksum

def filewithheader():
    start = time.time()
    file = open("DataSent.txt", "rb") # opening file in binary
    line = file.read(bfsize)
    print("Sending file...")
    time.sleep(0.5)

    while(line):
        length = len(line)
        # calculating checksum using zlib
        checksum = addChecksum(line)
        # packing all 
        header = struct.pack("!IIII", sport, rport, length, checksum)
        fullpacket = header + line               # concatinating header and data
        sender.sendto(bytes(fullpacket), raddress)
        # reading remaining data from file 
        line = file.read(bfsize)

    # closing file
    file.close()
    end = time.time()
    elapsed = end - start  
    print("File Transferred Succesfully")
    time.sleep(0.5)

    # printing stats
    print("Transfer time = ", elapsed)

# function calls
filewithheader()