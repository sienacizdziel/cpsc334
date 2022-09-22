import RPi.GPIO as GPIO
import time

def button_callback(channel):
    print("Button was pushed!")

switchPin = 17
buttonPin = 23
joystickPin = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(switchPin, GPIO.IN)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(joystickPin, GPIO.IN)

print("starting...")

GPIO.add_event_detect(buttonPin,GPIO.RISING,callback=button_callback)

try:
    while 1:
        if not GPIO.input(switchPin):
            print("switch toggled!")
            print(GPIO.input(switchPin))
            print("joystick pin: " + str(GPIO.input(joystickPin)))
        time.sleep(2)
        
except KeyboardInterrupt:
    GPIO.cleanup()

