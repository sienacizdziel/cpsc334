import socket
SHARED_UDP_PORT = 4210
UDP_IP = "172.29.33.215"
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet  # UDP
sock.bind((UDP_IP, SHARED_UDP_PORT))
while True:
    data, addr = sock.recvfrom(1024)
    print(data)
