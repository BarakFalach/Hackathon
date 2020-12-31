
import socket
import struct
import sys
import msvcrt
import time
import select






# The Game is on 
# input: server connection that the game is occuring on.
def start_clicking(server):
    # readable, writable, exceptional = select.select(inputs, outputs, inputs)
    # print("start clicking!!!")
    dead_line = time.time() + 10
    # while time.time() < dead_line:
    #     if msvcrt.kbhit():
    #         pressedKey = msvcrt.getch()
    #         s.sendall(pressedKey)
    # print('stop clicking!')
    # the_winner_is = s.recv(1024).decode()
    # print(the_winner_is)
    inputs = [server]
    outputs = []
    flag=True
    try:
        while flag:
            readable, writable, exceptional = select.select(inputs, outputs, inputs,0.01)
            for s in readable:
                if s is server: 
                    the_winner_is = s.recv(1024).decode()
                    print(the_winner_is)
                    flag = False
                    break
            if msvcrt.kbhit():
                pressedKey = msvcrt.getch()
                server.sendall(pressedKey)
    except:
        print ("cient Except")
        pass



# ask the host to join the game sending the client name
# input: the host ip that has broadcated , the port num that the host sent, the client name
def establish_TCP(host_ip, port_to_connect,client_name):
    HOST = host_ip  # The server's hostname or IP address
    PORT = port_to_connect        # The port used by the server
    # print("Host_ip: "+str(host_ip)+", port_to_connect: "+ str(port_to_connect))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # print("before connection")
        s.connect((HOST, PORT))
        # print("after connection before sending")
        s.sendall((client_name +"\n").encode())
        data = s.recv(1024).decode()
        print(data)
        start_clicking(s)
        
    







client_name = "cheesy_crust"

while True:
    
    UdpClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UdpClient.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    UdpClient.bind(('', 13117))
    print("Client started, listening for offer requests...")
    # wrong: mreq = struct.pack("sl", socket.inet_aton("224.51.105.104"), socket.INADDR_ANY)

    msg_from_server , b = UdpClient.recvfrom(28)
    msg = struct.unpack('Ibh', msg_from_server)
    # print (str(msg))
    # print (b)
    print("Received offer from "+b[0] +" attempting to connect...")

    establish_TCP(b[0],msg[2],client_name)
    print("Server Disconnected")
