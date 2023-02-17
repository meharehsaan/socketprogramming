# https://github.com/meharehsaan
import socket
import sys
import random

RECEIVER_ADDR = ('localhost', 8080)

def make(seq_num, data = b''):
    seq_bytes = seq_num.to_bytes(4, byteorder = 'little', signed = True)
    return seq_bytes + data

# Extracts sequence number and data from a non-empty packet
def extract(packet):
    seq_num = int.from_bytes(packet[0:4], byteorder = 'little', signed = True)
    return seq_num, packet[4:]

DROP_PROB = 8

def send(packet, sock, addr):
    if random.randint(0, DROP_PROB) > 0:
        sock.sendto(packet, addr)
    return

# Receive a packet from the unreliable channel
def recv(sock):
    packet, addr = sock.recvfrom(1024)
    return packet, addr

# Receive packets from the sender
def receive(sock, filename):
    # Open the file for writing
    try:
        file = open(filename, 'wb')
    except IOError:
        print('Unable to open', filename)
        return
    
    expected_num = 0
    while True:
        # Get the next packet from the sender
        pkt, addr = recv(sock)
        if not pkt:
            break
        seq_num, data = extract(pkt)
        print('Got packet', seq_num)
        
        # Send back an ACK
        if seq_num == expected_num:
            print('Got expected packet')
            print('Sending ACK', expected_num)
            pkt = make(expected_num)
            send(pkt, sock, addr)
            expected_num += 1
            file.write(data)
        else:
            print('Sending ACK', expected_num - 1)
            pkt = make(expected_num - 1)
            send(pkt, sock, addr)

    file.close()

# Main function
if __name__ == '__main__':
    # if len(sys.argv) != 2:
    #     print('Expected filename as command line argument')
    #     exit()
        
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(RECEIVER_ADDR) 
    # filename = sys.argv[1]
    filename = "DataReceived.txt"

    receive(sock, filename)
    sock.close()