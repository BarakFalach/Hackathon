
import socket
import struct

UdpClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UdpClient.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
UdpClient.bind(('', 3000))

 # wrong: mreq = struct.pack("sl", socket.inet_aton("224.51.105.104"), socket.INADDR_ANY)

while True:
    msg_from_server , b = UdpClient.recvfrom(28)
    msg = struct.unpack('Ibh', msg_from_server)
    print (str(msg))