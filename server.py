import concurrent.futures
import socket
import time
import struct
import sys
import threading
from Player import Player

gameOn = False
thread_counter = 0
gameEnded = False
HOST = '192.168.0.68'  
TCP_PORT = 5000       
UDP_PORT = 3000

def game_print(game_teams,start,group1=False,group2=False): 
    string_builder = ""
    if start:
        string_builder += "Welcome to Keyboard Spamming Battle Royale."
    if start or group1:
        string_builder+="\nGroup 1:\n==\n"
        for player in game_teams[0]:
            string_builder += f"{player.teamName}\n"
    if start or group2:
        string_builder += "Group 2:\n==\n"
        for player in game_teams[1]:
            string_builder += f"{player.teamName}\n"
    if start:
        string_builder += "Start pressing keys on your keyboard as fast as you can!!"
    else:
        string_builder += "Congratulations to the winners\nSee you next Time!"
    return string_builder
def winner_messege_print(result,game_teams):
    string_builder =f"Game Over!\n{result[0][0]} typed in: {result[0][1]}.  {result[1][0]} typed in: {result[1][1]}\n"
    if result[0][0] == "Group_1":
        string_builder += "Group 1 Won!\n"
        string_builder+=game_print(game_teams,False,True,False)
    else:
        string_builder += "Group 2 Won!\n"
        string_builder+=game_print(game_teams,False,False,True)
    return string_builder
        

def endGame (game_teams):
    global gameEnded
    global gameOn
    result =  [["Group_1",0],["Group_2",0]]
    team_to_add = 0
    gameOn=False
    time.sleep(1)
    for team in game_teams:
        for player in team:
            result[team_to_add][1] += player.score
        team=1
    result = sorted(result,key=lambda x: x[1],reverse=True)
    winner_messege = winner_messege_print(result,game_teams)
    print(winner_messege)
    for team in game_teams:
        for player in team:
            player.connection.sendall(winner_messege.encode())
            player.connection.close()
    gameEnded = True
    


def loadingPrint(count=0):
    count = str(count)
    bar = [
    " [="+count+"               ]",
    " [=="+count+"              ]",
    " [==="+count+"             ]",
    " [===="+count+"            ]",
    " [====="+count+"           ]",
    " [======"+count+"          ]",
    " [======="+count+"         ]",
    " [========"+count+"        ]",
    " [========="+count+"       ]",
    " [=========="+count+"      ]",
    " [==========="+count+"     ]",
    " [============"+count+"    ]",
    " [============="+count+"   ]",
    " [=============="+count+"  ]",
    " [==============="+count+" ]",
    " [================"+count+"]",
    
    
    ]
    for i in range (0,len(bar)):
        print(bar[i % len(bar)], end="\r")
        time.sleep(0.06)
    

def game_room(current_player:Player,msg):
    global gameOn
    global thread_counter
    print (f"---waiting room--- \n welcome: {current_player.teamName}")
    connection = current_player.connection 
    connection.sendall(msg.encode())
    start = time.time()
    connection.settimeout(10.5)
    while (time.time() < start+10):
        try:
            print (f"start: {start}")
            data = connection.recv(8)
            print (f"end: {time.time()}")
            current_player.score += 1
        except:
            print ("GOT EXCEPT")
            current_player.flag=False
            thread_counter-=1
            return
    thread_counter-=1
    return
            


def boradcast():
    global gameOn
    global TCP_PORT
    global UDP_PORT
    global HOST
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.settimeout(0.2)
    message = struct.pack("Ibh",0xfeedbeef,0x2,TCP_PORT)
    count_down = 10 
    print (f"“Server started, listening on IP address {HOST}")
    while (count_down):
        server.sendto(message, ('<broadcast>', UDP_PORT))
        loadingPrint(11-count_down)
        # time.sleep(1)
        count_down-=1
    server.close()
    gameOn = True

        
def tcp_connection():
    global gameOn
    global thread_counter
    global HOST
    global TCP_PORT
    group_to_enter = 0 
    print ("TCP Connection ")
    game_teams  = []
    team_1 = []
    team_2 = []
    game_teams.append(team_1)
    game_teams.append(team_2)
    tcp_server =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server.bind((HOST, TCP_PORT))
    tcp_server.listen()
    tcp_server.settimeout(11)
    
    while not gameOn:
        try:
            print ("Before TCP")
            conn, addr = tcp_server.accept()
            new_player = Player(conn,addr)
            game_teams[group_to_enter].append(new_player)
            group_to_enter = (group_to_enter+1)%2
            data = conn.recv(1024)
            tName = data.decode()
            new_player.teamName=tName
            print (f"Crete Player {new_player.teamName} ")
        except:
            print ("Loby Closed, Gaem Will Start Soon")
            gameOn = True
    msg = game_print(game_teams,True)
    for team in game_teams:
        for player in team:
            thread_counter+=1
            player.thread = threading.Thread(target=game_room,args=[player,msg])
            player.thread.start()
    while (thread_counter>0):
        print (thread_counter)
        time.sleep(0.5)
    
    endGame(game_teams)
    tcp_server.close()




def run_server():
    global gameEnded
    print ("---Ostrov and Falach Server---")
    t1 = threading.Thread(target=boradcast)
    t2 = threading.Thread(target=tcp_connection)    
    t2.start()
    t1.start()
    # t1.start()
    while not gameEnded:
        time.sleep(1)
    print (f"End Game !")
        

            




# t1 = threading.Thread(target=boradcast)
# t2 = threading.Thread(target=tcp_connection)
while True:
    gameOn = False
    gameEnded = False
    thread_counter = 0
    run_server()


