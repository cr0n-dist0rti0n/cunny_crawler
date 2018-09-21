import struct
import socket
import random
import os

private_ips = ('10.', '172.16.', '172.17.', '172.18.', '172.19.', '172.20.', '172.21', '172.22', '172.23', '172.24.', '172.25.', '172.26.', '172.27.', '172.28', '172.29', '172.30.', '172.31.', '192.168')        


def ipGeneration():
    ip = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
    while any(ext in ip for ext in private_ips):
        ip = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
    return ip 

def ipPick():
    response = 1
    while response != 0:
        hostname = str(ipGeneration())
        response = os.system('ping -c 1 ' + hostname + ' >/dev/null 2>&1')
    return hostname

