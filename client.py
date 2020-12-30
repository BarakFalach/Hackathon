
import socket
import struct
import sys

def establish_TCP():


    HOST = 'localhost'  # The server's hostname or IP address
    PORT = 65432        # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b'Hello, world')
        data = s.recv(1024)

    print('Received', repr(data))





# print("Client started, listening for offer requests...")
# UdpClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# UdpClient.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# UdpClient.bind(('', 3000))

#  # wrong: mreq = struct.pack("sl", socket.inet_aton("224.51.105.104"), socket.INADDR_ANY)

# msg_from_server , b = UdpClient.recvfrom(28)
# msg = struct.unpack('Ibh', msg_from_server)
# print (str(msg))
# print (b)
# print("Received offer from "+b[0] +" attempting to connect...")
establish_TCP()











