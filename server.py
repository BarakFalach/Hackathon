
import socket
import time
import struct
import sys
import threading
from Team import Team

def waiting_room():
    return None

def boradcast():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.settimeout(0.2)
    message = struct.pack("Ibh",1000,0x2,5000)
    count_down = 4 
    while (count_down):
        server.sendto(message, ('<broadcast>', 3000))
        print("message sent!")
        time.sleep(1)
        count_down-=1

        
def tcp_connection():
    
    print ("TCP Connection ")
    game_teams = [] 
    HOST = '192.168.0.68'  # Standard loopback interface address (localhost)
    PORT = 5000        # Port to listen on (non-privileged ports are > 1023)
    flag = True
    tcp_server =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server.bind((HOST, PORT))
    tcp_server.listen()
    while flag:
        conn, addr = tcp_server.accept()
        newTeam = Team(conn,addr)
        game_teams.append(newTeam)

        # t = threading.Thread(target=waiting_room)
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                tName = data.decode('utf-8')
                game_teams[0].teamName=tName
                if not data:
                    break
                conn.sendall(data)
                print (game_teams[0].teamName)
                print (tName)


print ("---Ostrove and Falach Server---")
t1 = threading.Thread(target=boradcast)
t2 = threading.Thread(target=tcp_connection)
t2.start()
t1.start()


