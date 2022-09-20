// dimensions
int screenHeight = 766;
int screenWidth = 4078;
int numScreens = 6;
int[] blocks = new int[numScreens];

// parameters
int t = 0;
int fr = 20;
int numWaves = 3;
float[] waveValues = new float[(int)Math.floor(screenHeight / numWaves) * 2];
//int[][] oceanColors = {{7, 74, 83}, {7, 115, 149}, "#5b9299", "#8dc1cf", "#aadbe1", "#b8bec0"};
//String[] sandColors = {"#f6d7b0", "#f2d2a9", "#eccca2", "#e7c496", "#e1bf92"};
int[] sandValues = new int[20];
String sand = null;
int numUmbrellas = 40;
Object[] umbrellaColors = new Object[numUmbrellas];
float[][] umbrellaLocations = new float[numUmbrellas][2];
String screen = "left";
String[] waveColors = new String[20];
int theta = 0;
float dx;

void setup() { 
  surface.setSize(screenWidth, screenHeight);
  surface.setLocation(-screenWidth, 0);
  //fullScreen();
  noFill();
  frameRate(20);
  dx = (TWO_PI / 500.0) * 3; 
  for (int i = 0; i < 20; i ++) {
    //waveColors[i] = oceanColors[round(random(oceanColors.length - 1))];
  }
  //sand = sandColors[floor(random(5))];
  //background(sand);
}

void draw() {
  stroke(255);
  strokeWeight(1);
  //fill(sand);
  //background(sand);
  createScreenSplits();

  if (screen == "left") {
    // for (int block = 0; block < 2; block += 1) {
      int waveCount = 0;
      for (int i = blocks[0] + 500; i < blocks[0] + 800; i += 80) {
        strokeWeight(10);
        if (t % 20 == 0) {
          //waveColors[waveCount] = oceanColors[round(random(oceanColors.length - 1))];
        }
        //fill(waveColors[waveCount]);
        //stroke(waveColors[waveCount]);
        calcWave();
        renderWave(i, 1, 2);
        waveCount++;
      }

      noFill();
      strokeWeight(20);
      stroke(255);
      curve(screenWidth, 50, screenWidth - 10, screenHeight, screenWidth - (screenWidth / numScreens / 2) + 50, 0, 200, 200);
      stroke(0);
      curve(5, 26, 0, 73, 24, 0, 73, 61, 0, 15, 65, 0);
      stroke(255, 102, 0);
      curve(73, 24, 0, 73, 61, 0, 15, 65, 0, 15, 65, 0);
    // }
  } else {
    int waveCount = 0;
    for (int i = blocks[1] + 500; i < blocks[1] + 800; i += 80) {
      strokeWeight(10);
      if (t % 20 == 0) {
        //waveColors[waveCount] = oceanColors[round(random(oceanColors.length - 1))];
      }
      //fill(waveColors[waveCount]);
      //stroke(waveColors[waveCount]);
      calcWave();
      renderWave(i, 2, 2);
      waveCount++;
    }
  }

  for (int i = 0; i < umbrellaColors.length; i++) {
    if (umbrellaColors[i] == null) {
      umbrellaColors[i] = color(floor(random(255)), floor(random(255)), floor(random(255)));
    }

    if (umbrellaLocations[i] == null) {
      float[] location = {random(1), random(1)};
      umbrellaLocations[i] = location;
    }
    //fill(umbrellaColors[i]);
    strokeWeight(0);

    push();
    translate(width * umbrellaLocations[i][0], height * umbrellaLocations[i][1]);
    rotate(frameCount / 30.0);
    polygon(0, 0, 50, 8);
    pop();

    stroke(255);
    strokeWeight(10);

    push();
    translate(width * umbrellaLocations[i][0], height * umbrellaLocations[i][1]);
    ellipse(0, 0, 1, 1);
    pop();
  }

  // frameRate(fr);
  t++;
}

void createScreenSplits() {
  for (int i = 0; i < numScreens; i++) {
    rect(screenWidth / numScreens * i, 0, screenWidth / numScreens, screenHeight);
    blocks[i] = screenWidth / numScreens * i;
  }
}

void calcWave() {
  theta += 0.02; 
  int y = theta;
  for (int i = 0; i < waveValues.length / 2; i++) {
    waveValues[i] = sin(y) * 75;
    y += dx;
  }
  y += 10;
  for (int i = waveValues.length / 2; i < waveValues.length; i++) {
    waveValues[i] = screenWidth / numScreens + sin(y) * 75;
    y += dx;
  }
}

void renderWave(int translateX, int block1, int block2) {
  for (int x = 0; x < waveValues.length / 2; x++) {
    ellipse(translateX + waveValues[x], x * numWaves, 40, 40);
  }
  coverBlock(block1);
  strokeWeight(10);

  for (int x = 0; x < waveValues.length / 2; x++) {
    ellipse(translateX + waveValues[waveValues.length / 2 + x], x * numWaves, 40, 40);
  }
  coverBlock(block2);

  // for (int x = 0; x < waveValues.length; x++) {
  //   ellipse(translateX * 2 + waveValues[x], x * numWaves, 40, 40);
  // }
}

void polygon(int x, int y, int radius, int npoints) {
  float angle = TWO_PI / npoints;
  beginShape();
  for (int a = 0; a < TWO_PI; a += angle) {
    float sx = x + cos(a) * radius;
    float sy = y + sin(a) * radius;
    vertex(sx, sy);
  }
  endShape(CLOSE);
}

void coverBlock(int block) {
  strokeWeight(0);
  //fill(sand);
  rect(blocks[block], 0, screenWidth / numScreens / 2, screenHeight);
}

void keyPressed() {
  if (keyCode == ENTER) {
    screen = "right";
  } else if (keyCode == BACKSPACE) {
    screen = "left";
  }
}
