import RPi.GPIO as GPIO
import time

# gpio input/output pins
switchPin = 17
buttonPin = 23
joystickPinX = 26
joystickPinY = 16
ledPin1 = 18
ledPin2 = 6

# mode 1 = spst switch off
ledPin1State = GPIO.LOW

# mode 2 = spst switch on
ledPin2State = GPIO.LOW

def button_callback(channel):
    print("Button was pushed!")
    global ledPin1State
    global ledPin2State

    # when in mode 1, change led 1 on button click
    if not GPIO.input(switchPin):
        if ledPin1State == GPIO.LOW:
            ledPin1State = GPIO.HIGH
        else:
            ledPin1State = GPIO.LOW
        GPIO.output(ledPin1, ledPin1State)

    # when in mode 2, change led 2 on button click
    else:
        if ledPin2State == GPIO.LOW:
            ledPin2State = GPIO.HIGH
        else:
            ledPin2State = GPIO.LOW
        GPIO.output(ledPin2, ledPin2State)

# gpio setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(switchPin, GPIO.IN)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(joystickPinX, GPIO.IN)
GPIO.setup(joystickPinY, GPIO.IN)
GPIO.setup(ledPin1, GPIO.OUT)
GPIO.setup(ledPin2, GPIO.OUT)

print("starting...")

GPIO.add_event_detect(buttonPin,GPIO.RISING,callback=button_callback)

# at the outset, light up led 1 if in mode 1, and led 2 if in mode 2
if not GPIO.input(switchPin):
    ledPin1State = GPIO.HIGH
    ledPin2State = GPIO.LOW
else:
    ledPin1State = GPIO.LOW
    ledPin2State = GPIO.HIGH
GPIO.output(ledPin1, ledPin1State)
GPIO.output(ledPin2, ledPin2State)

print(ledPin1State)
print(ledPin2State)

try:
    while 1:
        # listen for when both leds are on (mode 3)
        if ledPin1State == GPIO.HIGH and ledPin2State == GPIO.HIGH:
            # in mode 3, print continuously (digital )joystick positions
            print("joystick x: " + str(GPIO.input(joystickPinX)))
            print("joystick y: " + str(GPIO.input(joystickPinY)))
        time.sleep(1)
        
except KeyboardInterrupt:
    GPIO.cleanup()

