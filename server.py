
import socket
import time
import struct
import sys
import threading
from Player import Player

gameOn = False

def endGame (game_teams):
    global gameOn
    result =  [["Group_1",0],["Group_2",0]]
    team_to_add = 0
    gameOn=False
    for team in game_teams:
        for player in team:
            player.flag=False
    time.sleep(1)
    for team in game_teams:
        for player in team:
            result[team_to_add][1] += player.score
        team=1
    result = sorted(result,key=lambda x: x[1],reverse=True)
    winner_messege = f"{result[0][0]} Won you'r score is: {result[0][1]} , congrats"
    print(winner_messege)
    for team in game_teams:
        for player in team:
            player.connection.sendall(bytes(winner_messege,encoding='utf-8'))
    




def waiting_room(current_player:Player,msg):
    global gameOn
    print (f"---waiting room--- \n welcome: {current_player.teamName}")
    connection = current_player.connection 
    connection.sendall(bytes("hi Amit",encoding="utf-8"))
    while gameOn and current_player.flag:
        print (connection)
        data = connection.recv(8)
        print (data.decode('utf-8'))
        current_player.score += 1

        


def boradcast():
    global gameOn
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.settimeout(0.2)
    message = struct.pack("Ibh",0xfeedbeef,0x2,5000)
    count_down = 5 
    while (count_down):
        server.sendto(message, ('<broadcast>', 3000))
        print("message sent!")
        time.sleep(1)
        count_down-=1
    server.close()
    gameOn = True

        
def tcp_connection():
    global gameOn
    group_to_enter = 0 
    print ("TCP Connection ")
    game_teams  = []
    team_1 = []
    team_2 = []
    game_teams.append(team_1)
    game_teams.append(team_2)
    HOST = '192.168.0.68'  # Standard loopback interface address (localhost)
    PORT = 5000        # Port to listen on (non-privileged ports are > 1023)
    tcp_server =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server.bind((HOST, PORT))
    tcp_server.listen()
    tcp_server.settimeout(5)
    
    while not gameOn:
        try:
            print ("Before TCP")
            conn, addr = tcp_server.accept()
            new_player = Player(conn,addr)
            game_teams[group_to_enter].append(new_player)
            group_to_enter = (group_to_enter+1)%2
            data = conn.recv(1024)
            tName = data.decode('utf-8')
            new_player.teamName=tName
            print (f"Crete Player {new_player.teamName} ")
        except:
            pass
            gameOn = True
        # t = threading.Thread(target=waiting_room,args=[new_player])
        # new_player.thread=t
        # t.start()

        # print ("after Thread Start")
        # time.sleep(5)
        # game_teams[0].flag=False
        # game_teams[0].connection.sendall(bytes(f"your Player score is {game_teams[0].teamName}"))
        # time.sleep(1)
        # game_teams[0].connection.close()

        # print ("flag change to false")
        # game_teams[0].connection.close()
        # gameOn = False
        # game_teams[0].connection.close()
        # flag=False
    msg = f""
    for team in game_teams:
        for player in team:
            t = threading.Thread(target=waiting_room,args=[player])
            player.thread=t
            t.start()
    time.sleep(6)
    endGame(game_teams)
        

            




print ("---Ostrove and Falach Server---")
t1 = threading.Thread(target=boradcast)
t2 = threading.Thread(target=tcp_connection)
t2.start()
t1.start()


