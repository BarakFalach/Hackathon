
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

    HOST = 'localhost'  # Standard loopback interface address (localhost)
    PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)

        


print ("---Ostrove and Falach Server---")
tcp_connection()

