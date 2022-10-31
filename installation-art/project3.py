from guizero import App, Drawing
import RPi.GPIO as GPIO
import socket 
import random
import copy

# set up web socket
SHARED_UDP_PORT = 4210
UDP_IP = "172.29.33.215" # ip of raspi (changes by location)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, SHARED_UDP_PORT))
touch1, touch2, touch3, light1, light2 = None, None, None, None, None
prev_touch1, prev_touch2, prev_touch3 = None, None, None
prev_light1, prev_light2 = None, None

# colors
bg_color_scheme = [(11, 9, 9), (68, 68, 76), (140, 140, 140), (214, 214, 214)]
shape_color_scheme = [(16, 21, 27), (85, 90, 100), (173, 179, 189), (132, 148, 158), (75, 92, 116)]
color = 0
color2 = 1
num_colors1 = 4
num_colors2 = 5
oval_id = None

# lines
touch_change = 8
lines = {}
size = 100
width = 3

def general_callback():
    global touch1, touch2, touch3, light1, light2
    global color, color2, lines, size
    global prev_touch1, prev_touch2, prev_touch3, prev_light1, prev_light2

    # receive data from esp32
    data, addr = sock.recvfrom(1024)
    data = (data.decode("utf-8")).split(',')
    prev_touch1, prev_touch2, prev_touch3 = touch1, touch2, touch3
    prev_light1, prev_light2 = light1, light2
    touch1, touch2, touch3, light1, light2 = int(data[0]), int(data[1]), int(data[2]), int(data[3]), int(data[4])
    
    # update colors and add points by touch
    if prev_touch1 > touch1 + touch_change:
        app.bg = bg_color_scheme[color]
        color = (color + 1) % num_colors1
    if prev_touch2 > touch2 + touch_change:
        x = random.randint(0, 700)
        line_id = d.line(x, -size, x, 0, color=shape_color_scheme[color2], width=width)
        lines[line_id] = (x, -size, x, 0, shape_color_scheme[color2])
    if prev_touch3 > touch3 + touch_change:
        print("touch 3")
        color2 = (color2 + 1) % num_colors2
        new_dict = {}
        for line in lines.keys():
            if random.randint(0, 1):
                d.delete(line)
                x1, y1, x2, y2, line_color = lines[line]
                new_line_id = d.line(x1, y1, x2, y2, color=shape_color_scheme[color2], width=width)
                new_dict[new_line_id] = (x1, y1, x2, y2, shape_color_scheme[color2])
            else:
                new_dict[line] = lines[line]
        lines = copy.deepcopy(new_dict)

    # movement affects line shift speed
    light_sensitivity = 15
    speed = 5
    if prev_light1 > light1 + light1 / light_sensitivity or prev_light1 < light1 / light_sensitivity:
        speed = -speed
    elif prev_light2 > light2 + light2 / light_sensitivity or prev_light2 < light2 / light_sensitivity:
        speed = speed
    else:
        speed = 0

    # shift lines 
    new_dict = {}
    for line in lines.keys():
        # adding randomness to lines chosen
        if random.randint(0, 1):
            d.delete(line)
            x1, y1, x2, y2, line_color = lines[line]
            if x2 + speed > 710 or x1 - speed < 0:
                continue
            new_line_id = d.line(x1 + speed, y1, x2 + speed, y2, color=line_color, width=width)
            new_dict[new_line_id] = (x1 + speed, y1, x2 + speed, y2, line_color)
        else:
            new_dict[line] = lines[line]
    lines = copy.deepcopy(new_dict)

def move_lines():
    # repeatedly moves points downwards
    global lines
    speed = 5
    new_dict = {}
    for line in lines.keys():
        d.delete(line)
        x1, y1, x2, y2, line_color = lines[line]
        if y2 + speed > 490 + size:
            continue
        #new_color = shape_color_scheme[color2] if random.randint(0, 1) else line_color
        new_line_id = d.line(x1, y1 + speed, x2, y2 + speed, color=line_color, width=width)
        new_dict[new_line_id] = (x1, y1 + speed, x2, y2 + speed, line_color)
    lines = copy.deepcopy(new_dict)

def exit_program():
   exit()

if __name__ == '__main__':
    # get initial data from esp32
    data, addr = sock.recvfrom(1024)
    data = (data.decode("utf-8")).split(',')
    touch1, touch2, touch3, light1, light2 = int(data[0]), int(data[1]), int(data[2]), int(data[3]), int(data[4])
    prev_touch1, prev_touch2, prev_touch3 = touch1, touch2, touch3
    prev_light1, prev_light2 = light1, light2

    # app settings
    app = App('installation art', bg=bg_color_scheme[color])
    app.set_full_screen()

    # start drawing
    d = Drawing(app, width="fill", height="fill")
    d.repeat(100, move_lines)
    d.repeat(100, general_callback)
    d.when_clicked = exit_program

    app.display()
