
import socket
import struct
import sys
import msvcrt
import time


def start_clicking(s):
    # readable, writable, exceptional = select.select(inputs, outputs, inputs)
    print("start clicking!!!")
    dead_line = time.time() + 10
    while time.time() < dead_line:
         if msvcrt.kbhit():
            pressedKey = msvcrt.getch()
            s.sendall(pressedKey)
    print('stop clicking!')
    the_winner_is = s.recv(1024).decode()
    print(the_winner_is)    

def establish_TCP(host_ip, port_to_connect,client_name):


    HOST = host_ip  # The server's hostname or IP address
    PORT = port_to_connect        # The port used by the server
    print("Host_ip: "+str(host_ip)+", port_to_connect: "+ str(port_to_connect))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("before connection")
        s.connect((HOST, PORT))
        print("after connection before sending")
        s.sendall((client_name +"\n").encode())
        data = s.recv(1024).decode()
        print(data)
        start_clicking(s)
        
    






client_name = "cheesy_crust"
while True:
    print("Client started, listening for offer requests...")
    UdpClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UdpClient.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    UdpClient.bind(('', 3000))

    # wrong: mreq = struct.pack("sl", socket.inet_aton("224.51.105.104"), socket.INADDR_ANY)

    msg_from_server , b = UdpClient.recvfrom(28)
    msg = struct.unpack('Ibh', msg_from_server)
    print (str(msg))
    print (b)
    print("Received offer from "+b[0] +" attempting to connect...")

    establish_TCP(b[0],msg[2],client_name)











