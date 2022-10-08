# Interactive Device: Retro Sketch
## Siena Cizdziel

## Intro && Usage
Retro Sketch is an interactive art piece designed as a colorful, retro-style sketching device. To boot up the device, plug it in and click the on button for the Raspberry Pi. Next, double tap on the `interactive-art.sh` file on the Desktop of the Raspberry Pi and click "execute". This will run the program in full screen. 

To sketch a line, move the joystick. The button allows you to change the color of the line being created. Toggle the switch to switch between light and dark mode, which each have their own color schemes. 

To end the program, tap on the screen.

## Code Design
Inside of this repo, `esp32write.ino` is used to serial write joystick values from the ESP32 (which converted them from analog to digital), uploaded through the Arduino IDE. The bulk of the code for this program is written in `task2.py`, which uses the GUIzero library for graphics, reads from Serial for joystick values, and uses RPi.GPIO to read button and switch values from the Raspberry Pi GPIO. Finally, `interactive-art.sh` is a copy of the brief bash script I wrote that exists on Desktop to allow the user to easily start `task2.py` from Desktop on the display screen of the Raspberry Pi. 

## Video links:
Retro sketch 1: https://youtu.be/zJ-sk24o7_Y

Retro sketch 2: https://youtu.be/bmTvXZWNBQ0
