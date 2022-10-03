from guizero import App, Text, Drawing
import serial
import time
import RPi.GPIO as GPIO

# gpio pins
buttonPin = 16
switchPin = 26

# setup gpio
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin, GPIO.IN)
GPIO.setup(switchPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

# color schemes
night_bg = (54, 48, 98)
night_index = 0
night_colors = [(130, 115, 151), (77, 76, 125), (233, 213, 202)]
day_bg = (255, 192, 144)
day_index = 0
day_colors = [(127, 183, 126), (177, 215, 180), (247, 246, 220)]
color = (0, 0, 0)
mode = ""

def general_callback():
    print("here")
    global day_index, night_index, color, mode
    text.text_color = color
    text.value = text.text_color

    # switch color mode change
    if (not GPIO.input(switchPin)) and (mode == "night" or mode == ""):
        app.bg = day_bg
        day_index = (day_index + 1) % 3
        color = day_colors[day_index]
        mode = "day"
    elif GPIO.input(switchPin) and (mode == "day" or mode == ""):
        app.bg = night_bg
        night_index = (night_index + 1) % 3
        color = night_colors[night_index]
        mode = "night"

def button_change():
    # button line color change
    if GPIO.input(buttonPin) == 1:
        print("here")
        #point.bg = "blue"
    else:
        print("also here")
        #point.bg = "green"
        
def serial_coords():
    # read serial print coordinates
    line = (ser.readline().decode('utf-8').rstrip()).split(" ")
    x = int(line[1][:len(line[1]) - 1])
    y = int(line[3])
    print(x, y)

    #text.value = line

if __name__ == '__main__':
    app = App('interactive art')
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    ser.reset_input_buffer()

    # gpio events
    # GPIO.add_event_detect(buttonPin, GPIO.RISING, callback=color_change)

    #app.set_full_screen()

    text = Text(app, text="1", color=(233, 213, 202))
    text.repeat(1000, general_callback)

    # draw line using a point
    d = Drawing(app)
    point = d.oval(30, 30, 40, 40, color="black", outline=False, outline_color="black")
    d.repeat(100, button_change)
    d.repeat(1, serial_coords)

    # access serial print from esp32
    #ser = serial.Serial('/dev/ttylUSB0', 115200, timeout=1)
    #ser.reset_input_buffer()

    # listen for changes
    #while True:
    #    line = ser.readline().decode('utf-8').rstrip()

        

    app.display()
