import sys
import os
import threading
import socket
import time
import uuid
import struct
from datetime import datetime

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
server.bind(('', 0)) 
try:
    server.listen(20)
except socket.error:
    print('Failed to create socket')
    server.close()
# Leave broadcaster as a global variable.
broadcaster = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
broadcaster.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
broadcaster.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
# Setup the UDP socket


def send_broadcast_thread():
    node_uuid = get_node_uuid()
    while True:
        # TODO: write logic for sending broadcasts.
        broadcaster.sendto(node_uuid.encode("UTF-8"), ('', get_broadcast_port))
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
        data =  data.decode('UTF-8')
        print_blue(f"RECV: {data} FROM: {ip}:{port}")
        


def tcp_server_thread():
    """
    Accept connections from other nodes and send them
    this node's timestamp once they connect.
    """

    clientSocket, addr = server.accept()
    print("got a connection from %s" ,str(addr))
    t = time.time()
    t1 = time.gmtime(t) #calendar.timegm(tuple)




    pass


def exchange_timestamps_thread(other_uuid: str, other_ip: str, other_tcp_port: int):
    """
    Open a connection to the other_ip, other_tcp_port
    and do the steps to exchange timestamps.

    Then update the neighbor_info map using other node's UUID.
    """
    print_yellow(f"ATTEMPTING TO CONNECT TO {other_uuid}")
    pass


def daemon_thread_builder(target, args=()) -> threading.Thread:
    """
    Use this function to make threads. Leave as is.
    """
    th = threading.Thread(target=target, args=args)
    th.setDaemon(True)
    return th


def entrypoint():
    pass

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