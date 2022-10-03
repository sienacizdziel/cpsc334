import serial
import time

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    ser.reset_input_buffer()

    while True:
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
