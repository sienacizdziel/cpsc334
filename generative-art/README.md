# Module 1: Generative Art
# A Dynamic Beach Landscape, Siena Cizdziel

This is a dynamic generative art piece of an abstract aerial view of a beach. The code is written in Java in Processing (`generative_art_java.pde`) inside of the `generative_art_java` folder in this repository. 

*Note that this repo also contains obsolete code written in p5.js, which I couldn't bear to delete so I saved for posterity.*

# Code design
At the top of the `generative_art_java.pde` are many global variables that can be altered to change the code. Examples include the screen height and width, the number of umbrellas generated, and color schemes. 

All one-time setup code is done in the `setup()` function, including initialization. 

In `draw()` is the bulk of the program. `createScreenSplits()` splits the screen into the number of screens specified, in order to create a list of "blocks," which identify the screen pixel delineations between each window in LEEDS. Note that the code is written in a way that accounts for the 90 degree rotation of displays in LEEDS. 

Shapes in the sand are drawn first, anywhere on the screen. Waves are drawn using `calcWave()` and `renderWave()`, which uses parametrization and trigonometry to create sine waves that go from the center bottom to the top of each screen (again, accounting for 90 degree angles). Every 15 frames, the color changes according to the saved color scheme. Umbrella attributes are similarly saved, including boolean indicators for whether or not they are closing. Randomness plays a factor in when umbrellas open, close, move locations, and change colors. 

To generalize this code to different displays, you can change the screen height, screen width, and number of screens, using the `screenHeight`, `screenWidth`, and `numScreens` global variables. Changing the screen start location would require changing the `surface.setLocation()` values located in `setup()`. 

# Running the Code
* Open `generative_art_java.pde` (located inside the `generative_art_java` folder in this repo) in the Processing environment of the LEEDS computer.
* Turn on all projectors and ensure HDMI display cables are secured. 
* Click the play button at the top left of the Processing environment. 

The code is written to then automatically generate the art and display it at the appropriate location on the windows of LEEDS and with the corresponding size of the displays. 
