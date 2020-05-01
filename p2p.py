import sys
import os
import threading
import socket
import time
import uuid
import struct

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
broadcaster.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
broadcaster.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# Setup the UDP socket


def send_broadcast_thread(port):
    node_uuid = get_node_uuid()
    while True:
        # TODO: write logic for sending broadcasts.
        broadcaster.sendto(node_uuid.encode("UTF-8"), ('', port))
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
        daemon_thread_builder(exchange_timestamps_thread,(data,ip,port))


def tcp_server_thread(server):
    """
    Accept connections from other nodes and send them
    this node's timestamp once they connect.
    """
    server.listen(20)
    while True:
        clientSocket, addr = server.accept()
        print("got a connection from %s" ,str(addr))
        t = time.time() 
        packed = struct.pack("!f", t)       
        clientSocket.sendto(packed, addr)
    pass


def exchange_timestamps_thread(other_uuid: str, other_ip: str, other_tcp_port: int):
    """
    Open a connection to the other_ip, other_tcp_port
    and do the steps to exchange timestamps.

    Then update the neighbor_info map using other node's UUID.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((other_ip, other_tcp_port))
    if other_uuid in neighbor_information and neighbor_information[other_uuid].broadcast_count < 10:
        neighbor_information[other_uuid].broadcast_count += 1
    else:
        t = time.time()
        data, (ip, port) = sock.recvfrom(4096)
        t2 = data
        delay = t2 - t
        neighbor_information[other_uuid] = NeighborInfo(delay, 1, other_ip, other_tcp_port)
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
    server.bind(('', 0)) 
    port = server.getsockname()[1]
    daemon_thread_builder(tcp_server_thread, (server))
    daemon_thread_builder(send_broadcast_thread, (port)) 
    daemon_thread_builder(receive_broadcast_thread)
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