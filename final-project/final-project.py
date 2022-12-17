from guizero import App, Drawing, Text
import socket

# set up web socket
SHARED_UDP_PORT = 4210
UDP_IP = "172.29.33.169"
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, SHARED_UDP_PORT))

started = False
address = None
t1 = None
t2 = None
prev_data1 = None
prev_data2 = None

def on_click():
    global started
    if not started:
        started = True
        text.destroy()
    else:
        exit()

def general_callback():
    global t1, t2, prev_data1, prev_data2
    if not started:
        return
    data, addr = sock.recvfrom(1024)
    data = (data.decode("utf-8")).split(',')
    p1_score, p2_score = int(data[0]), int(data[1])
    print(p1_score, p2_score)
    if prev_data1 == p1_score and prev_data2 == p2_score:
        return
    if t1 and t2:
        t1.destroy()
        t2.destroy()
    t1 = Text(app, text=p1_score, color="red", bg="white", size=20, align="left", width=20, height=20)
    t2 = Text(app, text=p2_score, color="blue", bg="white", size=20, align="right", width=20, height=20)
    t1.when_clicked = exit_program
    t2.when_clicked = exit_program
    prev_data1 = p1_score
    prev_data2 = p2_score

def exit_program():
    if started:
        exit()


if __name__ == '__main__':
    data, addr = sock.recvfrom(1024)
    address = addr
    data = (data.decode("utf-8")).split(',')
    print(data)


    app = App('final project', bg='black')
    d = Drawing(app)
    d.repeat(200, general_callback)
    #drawing.rectangle(10, 10, 60, 60, color="blue")
    text = Text(app, text="start!", color="white", bg="blue", size=20, width=20, height=20)
    text.when_clicked = on_click
    d.when_clicked = exit_program
    app.set_full_screen()
    app.display()
    
