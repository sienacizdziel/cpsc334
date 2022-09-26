import RPi.GPIO as GPIO
import time

switchPin = 17
buttonPin = 23
joystickPin = 26
ledPin1 = 18
ledPin1State = GPIO.LOW
ledPin2 = 6
ledPin2State = GPIO.LOW

def button_callback(channel):
    print("Button was pushed!")
    global ledPin1State
    global ledPin2State

    # change state of led 1 in state 1 (switch open)
    if not GPIO.input(switchPin):
        if ledPin1State == GPIO.LOW:
            ledPin1State = GPIO.HIGH
        else:
            ledPin1State = GPIO.LOW
        GPIO.output(ledPin1, ledPin1State)

    # change state of led 2 in state 2 (switch closed)
    else:
        if ledPin2State == GPIO.LOW:
            ledPin2State = GPIO.HIGH
        else:
            ledPin2State = GPIO.LOW


GPIO.setmode(GPIO.BCM)
GPIO.setup(switchPin, GPIO.IN)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(joystickPin, GPIO.IN)
GPIO.setup(ledPin1, GPIO.OUT)
GPIO.setup(ledPin2, GPIO.OUT)

print("starting...")

GPIO.add_event_detect(buttonPin,GPIO.RISING,callback=button_callback)

# at the outset, light up led 1 if in state 1, and led 2 if in state 2
if not GPIO.input(switchPin):
    ledPin1State = GPIO.HIGH
    ledPin2State = GPIO.LOW
else:
    ledPin1State = GPIO.LOW
    ledPin2State = GPIO.HIGH
GPIO.output(ledPin1, ledPin1State)
GPIO.output(ledPin2, ledPin2State)

try:
    while 1:
        if not GPIO.input(switchPin):
            print("switch toggled!")
            print("joystick pin: " + str(GPIO.input(joystickPin)))
        time.sleep(2)
        
except KeyboardInterrupt:
    GPIO.cleanup()

