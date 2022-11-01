# Installation Art: Electric Chimes
## Siena Cizdziel
## Intro && Setup
Electric Chimes is an art installation in 2 separate pieces: a set of electric touch and motion-sensor "chimes" and an LED display. 
To start, hang the chimes in an accessible and open space. If you have batteries, connect them (with proper voltage regulation) by putting them inside the box attached to the chime and plugging them in via the open hole in the back of the box. If you only have a microUSB, plug that in to the ESP32 through the hole. Once powered, the ESP32 should automatically start sending sensor data. Next, plug in and turn on the Raspberry Pi. Once the display is booted, the program should automatically start running. To end the program, simply tap on the screen. 

## Usage
Lines slowly migrate down the display. When the middle sensor is touched, a line appears in a random x location at the top of the screen. When the leftmost sensor is touched, a random percentage of the lines moving on the screen will change color according to a color scheme. When the rightmost sensor is touched, the background changes color. When the motion sensors are activated via a change in light conditions, they will cause the lines to move left or right. 

## Code Design
In this repo, the code run on the ESP32 is `project3-sensors.ino`. The code reads sensor data from the specified GPIO pins and sends that information through UDP packets to the Raspberry Pi. The code that automatically runs on boot of the Raspberry Pi is inside `project3.py`. It reads the data sent to it from UDP packets and then uses that data to display graphical images through the Python guizero library. Finally, `run_program.sh` is the bash executable that runs as a `systemd` service on boot of the Raspberry Pi (once a graphical device is connected), so that there is no need to manually run the program once the Raspberry Pi is turned on. Any output from `project3.py` will go into `out.txt` for debugging.

## Troubleshooting
If the program is not automatically running on boot:
* Turn both the ESP32 and the Raspberry Pi off and on again.
* Make sure the IP addresses in `project3-sensors.ino` and `project3.py` are the same as the Raspberry Pi's current IP.

## Video Links
https://youtu.be/NAuVgHw1u2U 

https://youtu.be/lRBgOB5hRPQ
