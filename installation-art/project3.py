from guizero import App, Drawing
import RPi.GPIO as GPIO
import socket 
import random
import copy

# set up web socket
SHARED_UDP_PORT = 4210
UDP_IP = "172.29.135.237"
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, SHARED_UDP_PORT))
touch1, touch2, touch3, light1, light2 = None, None, None, None, None
prev_touch1, prev_touch2, prev_touch3 = None, None, None
prev_light1, prev_light2 = None, None

# leds
ledPin1 = 26
ledPin2 = 16
ledPin3 = 21
prev_cap = 0
capacitance = 0

# gpio setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin1, GPIO.OUT)
GPIO.setup(ledPin2, GPIO.OUT)
GPIO.setup(ledPin3, GPIO.OUT)

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
size = 30

def update_colors(is_bg):
    global color, color2, oval_id
    if is_bg:
        app.bg = bg_color_scheme[color]
        color = (color + 1) % num_colors1
    else:
        color2 = (color2 + 1) % num_colors2

def general_callback():
    global touch1, touch2, touch3, light1, light2, color, color2, prev_touch1, prev_touch2, prev_touch3, prev_light1, prev_light2, oval_id, color2, oval_coords
    data, addr = sock.recvfrom(1024)
    data = (data.decode("utf-8")).split(',')
    prev_touch1, prev_touch2, prev_touch3 = touch1, touch2, touch3
    prev_light1, prev_light2 = light1, light2
    touch1, touch2, touch3, light1, light2 = int(data[0]), int(data[1]), int(data[2]), int(data[3]), int(data[4])
    #print(touch1, touch2, touch3, light1, light2)
    
    # update background by touch
    print("prev_touch1" + str(prev_touch1) + " touch1" + str(touch1))
    if prev_touch1 > touch1 + touch_change:
        update_colors(0)
        print("one")
        x = random.randint(0, 50)
        line_id = d.oval(x, 50, x + size, 50 + size, color="white")
        lines[line_id] = (x, 40, x + size, 40 + size, shape_color_scheme[color2])
    if prev_touch2 > touch2 + touch_change:
        create_line(d)
    if prev_touch3 > touch3 + touch_change:
        update_colors(1)
        create_line(d)

    # update oval movement by movement
    '''if prev_light1 > light1 + light1 / 4 or prev_light1 < light1 / 4:
        d.delete(oval_id)
        new_oval_coord0 = oval_coords[0] + prev_light1 - light1
        if new_oval_coord0 < 0 or new_oval_coord0 + 50 > 800:
            new_oval_coord0 = oval_coords[0]
        new_oval_coord1 = oval_coords[1] + prev_light2 - light2
        if new_oval_coord1 < 0 or new_oval_coord1 + 50 > 800:
            new_oval_coord1 = oval_coords[1]
        oval_coords = (new_oval_coord0, new_oval_coord1, new_oval_coord0 + 50, new_oval_coord1 + 50)
        oval_id = d.oval(oval_coords[0], oval_coords[1], oval_coords[2], oval_coords[3], color=shape_color_scheme[color2])
        '''

def create_line(d):
    global lines
    print("create line")
    x = random.randint(0, 50)
    print(x, x + size)
    x = 50
    line_id = d.oval(x, 50, x + size, 50 + size, color="white")
    print(line_id)
    lines[line_id] = (x, 40, x + size, 40 + size, shape_color_scheme[color2])

def shift_lines():
    print("shifting")
    global lines
    new_dict = {}
    speed = 20
    for line in lines.keys():
        d.delete(line)
        x1, y1, x2, y2, line_color = lines[line]
        new_line_id = d.oval(x1 + speed, y1, x2 + speed, y2, line_color)
        new_dict[new_line_id] = (x1 + speed, y1, x2 + speed, y2, line_color)
    lines = copy.deepcopy(new_dict)

def move_lines():
    #print("moving")
    global lines
    speed = 5
    #new_dict = {}
    #for line in lines.keys():
        #d.delete(line)
        #x1, y1, x2, y2, line_color = lines[line]
        #print(lines[line])
        #new_line_id = d.oval(x1, y1 + speed, x2, y2 + speed, color=line_color, outline=False, outline_color=line_color)
        #new_dict[new_line_id] = (x1, y1 + speed, x2, y2 + speed, line_color)
    #lines = copy.deepcopy(new_dict)
    #print(lines)

def exit_program():
   exit()

if __name__ == '__main__':
    # get initial data from esp32
    data, addr = sock.recvfrom(1024)
    data = (data.decode("utf-8")).split(',')
    touch1, touch2, touch3, light1, light2 = int(data[0]), int(data[1]), int(data[2]), int(data[3]), int(data[4])
    prev_touch1, prev_touch2, prev_touch3 = touch1, touch2, touch3
    prev_light1, prev_light2 = light1, light2

    # initially light leds
    GPIO.output(ledPin2, GPIO.HIGH)
    GPIO.output(ledPin3, GPIO.HIGH)
    GPIO.output(ledPin1, GPIO.HIGH)

    # app settings
    app = App('installation art', bg=bg_color_scheme[color])
    #app.set_full_screen()

    # start drawing
    d = Drawing(app, width="fill", height="fill")
    #d.repeat(100, move_lines)
    d.repeat(1, general_callback)

    d.when_clicked = exit_program

    app.display()
