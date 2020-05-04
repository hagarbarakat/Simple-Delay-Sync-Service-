import sys
import os
import threading
import socket
import time
import uuid
import struct
import datetime

# https://bluesock.org/~willkg/dev/ansi.html
ANSI_RESET = "\u001B[0m"
ANSI_RED = "\u001B[31m"
ANSI_GREEN = "\u001B[32m"
ANSI_YELLOW = "\u001B[33m"
ANSI_BLUE = "\u001B[34m"

_NODE_UUID = str(uuid.uuid4())[:8]


def print_yellow(msg):
    print(f"{ANSI_YELLOW}{msg}{ANSI_RESET}")


def print_blue(msg):
    print(f"{ANSI_BLUE}{msg}{ANSI_RESET}")


def print_red(msg):
    print(f"{ANSI_RED}{msg}{ANSI_RESET}")


def print_green(msg):
    print(f"{ANSI_GREEN}{msg}{ANSI_RESET}")


def get_broadcast_port():
    return 35498


def get_node_uuid():
    return _NODE_UUID


class NeighborInfo(object):
    def __init__(self, delay, broadcast_count, ip=None, tcp_port=None):
        # Ip and port are optional, if you want to store them.
        self.delay = delay
        self.broadcast_count = broadcast_count
        self.ip = ip
        self.tcp_port = tcp_port


############################################
#######  Y  O  U  R     C  O  D  E  ########
############################################


# Don't change any variable's name.
# Use this hashmap to store the information of your neighbor nodes.
neighbor_information = {}

# Leave the server socket as global variable.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Leave broadcaster as a global variable.
broadcaster = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
broadcaster.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
broadcaster.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
broadcaster.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# Setup the UDP socket


def send_broadcast_thread():
    node_uuid = get_node_uuid()
    while True:
        # TODO: write logic for sending broadcasts.
        port = server.getsockname()[1]
        print_red(f"{node_uuid} is sending broadcast with port {port}...")
        packed = struct.pack("!8s4si",node_uuid.encode("UTF-8"), " ON ".encode("UTF-8"), port) 
        broadcaster.sendto(packed, ('255.255.255.255', get_broadcast_port()))
        time.sleep(1)   # Leave as is.


def receive_broadcast_thread():
    """
    Receive broadcasts from other nodes,
    launches a thread to connect to new nodes
    and exchange timestamps.
    """
    while True:
        # TODO: write logic for receiving broadcasts.
       
        data, (ip, port) = broadcaster.recvfrom(4096)
        data =  struct.unpack('!8s4si', data)
        print(data[0].decode('UTF-8'), data[1].decode('UTF-8'), data[2])
        print_blue(f"RECV: {data} FROM: {ip}:{port}")
        thread_4 = daemon_thread_builder(exchange_timestamps_thread, (data[0].decode('UTF-8'), ip, data[2]))
        thread_4.start()


def tcp_server_thread():
    """
    Accept connections from other nodes and send them
    this node's timestamp once they connect.
    """
    server.listen(20)
    while True:
        clientSocket, addr = server.accept()
        print("[TCP Server] got connection from: ", str(addr))
        t = datetime.datetime.utcnow().timestamp()
        #print_yellow(f"current node {get_node_uuid()} timestamp = {t}")
        packed = struct.pack("!d", t) 
        clientSocket.send(packed)
        clientSocket.close()


def exchange_timestamps_thread(other_uuid: str, other_ip: str, other_tcp_port: int):
    """
    Open a connection to the other_ip, other_tcp_port
    and do the steps to exchange timestamps.

    Then update the neighbor_info map using other node's UUID.
    """
    node = get_node_uuid()
    if node.strip() == other_uuid.strip():
        return
    if other_uuid in neighbor_information and neighbor_information[other_uuid].broadcast_count < 10:
        print_red(f"counter = {neighbor_information[other_uuid].broadcast_count}")
        neighbor_information[other_uuid].broadcast_count += 1
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((other_ip, other_tcp_port))
        print_yellow(f"ATTEMPTING TO CONNECT TO {other_uuid}")
        time.sleep(1)
        data = sock.recv(4096)
        unpacked = struct.unpack("!d", data)
        t2 = unpacked[0]
        print_green(f"current node {get_node_uuid()} timestamp: {t2}")
        t = datetime.datetime.utcnow().timestamp()
        print(f"other node {other_uuid} timestamp: {t}") 
        delay = t - t2
        print("Delay = ",delay)
        neighbor_information[other_uuid] = NeighborInfo(delay, 1, other_ip, other_tcp_port)
        sock.close()


def daemon_thread_builder(target, args=()) -> threading.Thread:
    """
    Use this function to make threads. Leave as is.
    """
    th = threading.Thread(target=target, args=args)
    th.setDaemon(True)
    return th


def entrypoint():
    broadcaster.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    broadcaster.bind(('255.255.255.255', get_broadcast_port()))
    server.bind(("0.0.0.0", 0)) 
    thread_1 = daemon_thread_builder(tcp_server_thread)
    thread_2 = daemon_thread_builder(send_broadcast_thread) 
    thread_3 = daemon_thread_builder(receive_broadcast_thread)
    thread_1.start()
    thread_2.start()
    thread_3.start()
    thread_1.join()
    thread_2.join()
    thread_3.join()
    


############################################
############################################


def main():
    """
    Leave as is.
    """
    print("*" * 50)
    print_red("To terminate this program use: CTRL+C")
    print_red("If the program blocks/throws, you have to terminate it manually.")
    print_green(f"NODE UUID: {get_node_uuid()}")
    print("*" * 50)
    time.sleep(2)   # Wait a little bit.
    entrypoint()


if __name__ == "__main__":
    main()
