# Final Project: Marble Battle
## Siena Cizdziel

## Intro && Gameplay
Marble Battle is a 2-player competitive interactive game that resembles pong (the video game) but in real life and with marbles! Each player has a controller with two buttons, one to flip your paddle and the other to "shake it up!", which shakes the board in case the marble gets stuck. To play, hit the marble back and forth across the board, defending your own goal and aiming to hit the marble into your opponent's goal. Once a point is scored, no more points can be scored until a paddle moves again (i.e. gameplay has continued), to prevent accidental repeat points. To win, score more points than your opponent!

To start the game, plug in the game board (a USB-C cord) to a computer. If you also want to see scoring, plug in the Raspberry Pi to an outlet, and the display should boot up and run the program automatically. To start the scoring, tap on the screen when it shows a blue button labeled “Start”.

If you'd like to reset scores, simply unplug and replug the cord attached to the game. 

To turn off the game, simply unplug everything. 

As you’ll see in the demo video, the largest marble (about double the size of the small ones in the photo above) actually does much better in this game’s mechanics than the smaller ones!

## Code Design

`cs334_final_project` contains the Arduino code loaded onto the ESP32. This code powers the stepper motors, reads from the buttons and photoresistor sensors, and keeps track of scores, before sending those scores via wifi UDP packets to the Raspberry Pi. The motors are run in two different tasks via multithreading, so that players can move both steppers at once. Towards the top of the code, in addition to constants defined for GPIO pins, there are several variables that can be adjusted to account for delay times (i.e. speed of paddle moving back and forth) and threshold (i.e. strength of the change in light that is needed to add a point, in case of different lighting conditions).

`final_project.py` is the code that is run on the Raspberry Pi on boot. This code listens for information from the ESP32 and then uses the GUIZero package to display that score information on a 5-inch LED touchscreen. 

Finally `run_program.sh` runs this program on boot on the Raspberry Pi.

To recreate this code, be sure to go into `cs334_final_project` and `final_project.py` to update the IP addresses stored there with your Raspbery Pi's new IP address. This allows for web communication to successfully occur via sockets. 

## Video
https://youtu.be/Tn2R0LLsmZs
