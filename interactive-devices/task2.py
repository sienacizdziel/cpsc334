from guizero import App, Text, Drawing, PushButton
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
night_bg = (24, 24, 24)
night_index = 0
night_colors = [(135, 88, 255), (92, 184, 228), (242, 242, 242)]
day_bg = (252, 226, 219)
day_index = 0
day_colors = [(255, 143, 177), (178, 112, 162), (122, 68, 149)]
color = None
mode = ""

# point location
x1 = 30
y1 = 30
x2 = 40
y2 = 40
ovals = []

def general_callback():
    global day_index, night_index, color, mode

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
    global color, night_index, day_index

    # button line color change
    if GPIO.input(buttonPin) == 0:
        if mode == "day":
            color = day_colors[day_index]
            day_index = (day_index + 1) % 3
        else:
            color = night_colors[night_index]
            night_index = (night_index + 1) % 3
        #d.oval(x1, y1, x2, y2, color=color, outline=False, outline_color=color)
        
def serial_coords():
    global x1, y1, x2, y2, ovals

    # read serial print coordinates
    line = (ser.readline().decode('utf-8').rstrip()).split(" ")
    print(line)
    x = int(line[1][:len(line[1]) - 1])
    y = int(line[3])
    
    speed = 1
    changed = False
    if x > 0 and x2 < 800:
        x1 += speed
        x2 += speed 
        changed = True
    elif x < -100 and x1 > 0:
        x1 -= speed
        x2 -= speed
        changed = True
    if y < 0 and y2 < 480:
        y1 += speed
        y2 += speed
        changed = True
    elif y > 200 and x != 3587 and y1 > 0:
        y1 -= speed
        y2 -= speed
        changed = True

    #print(changed)
    #print(x, y)
    if not changed:
        return
    oval_id = d.oval(x1, y1, x2, y2, color=color, outline=False, outline_color=color)
    ovals.append(oval_id)
    if len(ovals) > 10000:
        d.delete(ovals[0])
        ovals.remove(ovals[0])
    #print(ovals)

def exit_program():
   exit() 

if __name__ == '__main__':
    # initialize background
    if not GPIO.input(switchPin):
        bg = day_bg
    else:
        bg = night_bg

    # app settings
    app = App('interactive art', bg=bg)
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    ser.reset_input_buffer()
    #app.set_full_screen()

    d = Drawing(app, width="fill", height="fill")
    oval_id = d.oval(x1, y1, x2, y2, color=color, outline=False, outline_color=color)
    ovals.append(oval_id)
    d.repeat(1000, general_callback)
    d.repeat(100, button_change)
    d.repeat(1, serial_coords)

    d.when_clicked = exit_program

    app.display()
