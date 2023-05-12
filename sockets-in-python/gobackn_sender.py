# https://github.com/meharehsaan
import socket
import sys
import random
import socket
import _thread
import time

PACKET_SIZE = 512
RECEIVER_ADDR = ('localhost', 8080)
SENDER_ADDR = ('localhost', 0)
SLEEP_INTERVAL = 0.05
TIMEOUT_INTERVAL = 0.5
WINDOW_SIZE = 4

class Timer(object):
    TIMER_STOP = -1

    def __init__(self, duration):
        self._start_time = self.TIMER_STOP
        self._duration = duration

    # Starts the timer
    def start(self):
        if self._start_time == self.TIMER_STOP:
            self._start_time = time.time()

    # Stops the timer
    def stop(self):
        if self._start_time != self.TIMER_STOP:
            self._start_time = self.TIMER_STOP

    # Determines whether the timer is runnning
    def running(self):
        return self._start_time != self.TIMER_STOP

    # Determines whether the timer timed out
    def timeout(self):
        if not self.running():
            return False
        else:
            return time.time() - self._start_time >= self._duration

# Creates a packet from a sequence number and byte data
def make(seq_num, data = b''):
    seq_bytes = seq_num.to_bytes(4, byteorder = 'little', signed = True)
    return seq_bytes + data

# Creates an empty packet
def make_empty():
    return b''

# Extracts sequence number and data from a non-empty packet
def extract(packet):
    seq_num = int.from_bytes(packet[0:4], byteorder = 'little', signed = True)
    return seq_num, packet[4:]

DROP_PROB = 8

# Send a packet across the unreliable channel
# Packet may be lost
def send(packet, sock, addr):
    if random.randint(0, DROP_PROB) > 0:
        sock.sendto(packet, addr)
    return

# Receive a packet from the unreliable channel
def recv(sock):
    packet, addr = sock.recvfrom(1024)
    return packet, addr

# Shared resources across threads
base = 0
mutex = _thread.allocate_lock()
send_timer = Timer(TIMEOUT_INTERVAL)

# Sets the window size
def set_window_size(num_packets):
    global base
    return min(WINDOW_SIZE, num_packets - base)

# Send thread
def send_pck(sock, filename):
    global mutex
    global base
    global send_timer

    # Open the file
    try:
        file = open(filename, 'rb')
    except IOError:
        print('Unable to open', filename)
        return
    
    # Add all the packets to the buffer
    packets = []
    seq_num = 0
    while True:
        data = file.read(PACKET_SIZE)
        if not data:
            break
        packets.append(make(seq_num, data))
        seq_num += 1

    num_packets = len(packets)
    print('I gots', num_packets)
    window_size = set_window_size(num_packets)
    next_to_send = 0
    base = 0

    # Start the receiver thread
    _thread.start_new_thread(receive, (sock,))

    while base < num_packets:
        mutex.acquire()
        # Send all the packets in the window
        while next_to_send < base + window_size:
            print('Sending packet', next_to_send)
            # start = time.time()
            send(packets[next_to_send], sock, RECEIVER_ADDR)
            next_to_send += 1

        # Start the timer
        if not send_timer.running():
            # print('Starting timer')
            send_timer.start()

        # Wait until a timer goes off or we get an ACK
        while send_timer.running() and not send_timer.timeout():
            mutex.release()
            # print('Sleeping')
            time.sleep(SLEEP_INTERVAL)
            mutex.acquire()

        if send_timer.timeout():
            # Looks like we timed out
            print('Timeout')
            send_timer.stop();
            next_to_send = base
        else:
            print('Shifting window')
            window_size = set_window_size(num_packets)
        mutex.release()

    # Send empty packet as sentinel
    send(make_empty(), sock, RECEIVER_ADDR)
    # end = time.time()
    file.close()
    
# Receive thread
def receive(sock):
    global mutex
    global base
    global send_timer

    while True:
        pkt, _ = recv(sock);
        ack, _ = extract(pkt);

        # If we get an ACK for the first in-flight packet
        print('Got ACK', ack)
        if (ack >= base):
            mutex.acquire()
            base = ack + 1
            print('Base updated', base)
            send_timer.stop()
            mutex.release()

# Main function
if __name__ == '__main__':
    # if len(sys.argv) != 2:
    #     print('Expected filename as command line argument')

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(SENDER_ADDR)
    # filename = sys.argv[1]
    filename = "DataSent.txt"

    start = time.time()
    send_pck(sock, filename)
    end = time.time()
    sock.close()
    elapsed = end - start
    print(f"Time Taken {elapsed}")
    # print("Shutdowned")
