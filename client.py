
import socket
import struct
import sys

def establish_TCP():

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ("192.168.0.68", 5000)
    print ('connecting to %s port %s' % server_address)
    sock.connect(server_address)

    try:
        
        # Send data
        message = 'This is the message.  It will be repeated.'
        print ('sending "%s"' % message)
        sock.sendall(message)

        # Look for the response
        amount_received = 0
        amount_expected = len(message)
        
        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            print ('received "%s"' % data)

    finally:
        print ('closing socket')
        sock.close()





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
establish_TCP()











