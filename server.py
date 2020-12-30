
import socket
import time
import struct


server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
server.settimeout(0.2)
# server.bind(("localhost", 3000))
message = struct.pack("Ibh",1000,0x2,5000)
while True:
    server.sendto(message, ('<broadcast>', 3000))
    print("message sent!")
    time.sleep(1)