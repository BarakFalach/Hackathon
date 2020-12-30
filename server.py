
import socket
import time
import struct
import sys
from _thread import *
import threading

def boradcast():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.settimeout(0.2)
    message = struct.pack("Ibh",1000,0x2,5000)
    count_down = 10 
    while (count_down):
        server.sendto(message, ('<broadcast>', 3000))
        print("message sent!")
        time.sleep(1)
        count_down-=1
        
def tcp_connection():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 5000)
    sock.bind(server_address)
    print ("Before Bind")
    sock.listen(1)
    while True:
    # Wait for a connection
        print('waiting for a connection')
        connection, client_address = sock.accept()
        data = connection.recv(16)
        if data:
            print("Got Here")
            connection.sendall(data)

        


print ("---Ostrove and Falach Server---")
tcp_connection()

