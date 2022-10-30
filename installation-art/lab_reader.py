import socket
import RPi.GPIO as GPIO

ledPin = 26
ledPinState = GPIO.LOW

# setup gpio
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.OUT)

SHARED_UDP_PORT = 4210
UDP_IP = "172.29.135.237"
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet  # UDP
sock.bind((UDP_IP, SHARED_UDP_PORT))
while True:
    data, addr = sock.recvfrom(1024)
    print(data)
