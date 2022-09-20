// dimensions
int screenHeight = 766;
int screenWidth = 1360 * 6;
//int screenWidth = 2000;
int numScreens = 6;
int[] blocks = new int[numScreens];

int t = 0;
int fr = 20;
int numWaves = 8;
float[] waveValues = new float[(int)Math.floor(screenHeight / numWaves) * numScreens + 40];
int[][] oceanColors = {{7, 74, 83}, {7, 115, 149}, {91, 146, 153}, {141, 193, 207}, {170, 219, 225}, {184, 190, 192}};
int[] sandValues = new int[20];
int[] sand = {250, 231, 207};
int numUmbrellas = 80;
int[][] umbrellaColors = new int[numUmbrellas][3];
float[][] umbrellaLocations = new float[numUmbrellas][2];
String screen = "left";
int[][] waveColors = new int[20][3];
float theta = 0;
float dx;

void setup() { 
  surface.setSize(screenWidth, screenHeight);
  //surface.setLocation(1700, 0);
  //fullScreen();
  noFill();
  frameRate(20);
  dx = (TWO_PI / 500.0) * 3; 
  for (int i = 0; i < 20; i ++) {
    waveColors[i] = oceanColors[round(random(oceanColors.length - 1))];
  }
  background(sand[0], sand[1], sand[2]);
  
  // initializing umbrella values to null
  for (int i = 0; i < umbrellaColors.length; i++) {
    umbrellaColors[i] = null;
  }
  for (int i = 0; i < umbrellaLocations.length; i++) {
    umbrellaLocations[i] = null;
  }
}

void draw() {
  stroke(34, 34, 87);
  strokeWeight(1);
  fill(sand[0], sand[1], sand[2]);
  background(sand[0], sand[1], sand[2]);
  createScreenSplits();

  int waveCount = 0;
  for (int i = blocks[0] + 500; i < blocks[0] + 800; i += 80) {
    strokeWeight(10);
    if (t % 15 == 0) {
      waveColors[waveCount] = oceanColors[round(random(oceanColors.length - 1))];
    }
    fill(waveColors[waveCount][0], waveColors[waveCount][1], waveColors[waveCount][2]);
    stroke(waveColors[waveCount][0], waveColors[waveCount][1], waveColors[waveCount][2]);
    calcWave();
    renderWave(i);
    waveCount++;
  }

  for (int i = 0; i < umbrellaColors.length; i++) {
    if (umbrellaColors[i] == null) {
      int[] c = {floor(random(255)), floor(random(255)), floor(random(255))};
      umbrellaColors[i] = c;
    }

    if (umbrellaLocations[i] == null) {
      float[] location = {random(1), random(1)};
      umbrellaLocations[i] = location;
    }
    fill(umbrellaColors[i][0], umbrellaColors[i][1], umbrellaColors[i][2]);
    strokeWeight(0);

    pushMatrix();
    translate(width * umbrellaLocations[i][0], height * umbrellaLocations[i][1]);
    rotate(frameCount / 30.0);
    polygon(0, 0, 50, 8);
    popMatrix();
    
    stroke(0, 0, 0);
    strokeWeight(10);
    fill(0, 0, 0);
    
    pushMatrix();
    translate(width * umbrellaLocations[i][0], height * umbrellaLocations[i][1]);
    ellipse(0, 0, 1, 1);
    popMatrix();
  }

   frameRate(fr);
   t++;
}

void createScreenSplits() {
  strokeWeight(2);
  stroke(0);
  for (int i = 0; i < numScreens; i++) {
    rect(screenWidth / numScreens * i, 0, screenWidth / numScreens, screenHeight);
    blocks[i] = screenWidth / numScreens * i;
  }
}

void calcWave() {
  theta += 0.02; 
  float y = theta;
  for (int block = 0; block < numScreens; block++) {
    for (int i = 0; i < waveValues.length; i++) {
      waveValues[i] = sin(y) * 75;
      y += dx;
    }
  }
  // insert delay here
}

void renderWave(int translateX) {
  for (int i = 0; i < numScreens; i++) {
    for (int x = 0; x < waveValues.length / numScreens; x++) {
      ellipse(translateX + waveValues[waveValues.length / numScreens + x] + blocks[i], x * numWaves, 40, 40);
    }
    if (i + 1 != numScreens) {
      coverBlock(i + 1);
    }
    strokeWeight(10);
  }
}

void polygon(int x, int y, int radius, int npoints) {
  float angle = TWO_PI / npoints;
  beginShape();
  for (float a = 0; a < TWO_PI; a += angle) {
    float sx = x + cos(a) * radius;
    float sy = y + sin(a) * radius;
    vertex(sx, sy);
  }
  endShape(CLOSE);
}

void coverBlock(int block) {
  strokeWeight(0);
  fill(sand[0], sand[1], sand[2]);
  rect(blocks[block], 0, screenWidth / numScreens / 4, screenHeight);
}

void keyPressed() {
  if (keyCode == ENTER) {
    screen = "right";
  } else if (keyCode == BACKSPACE) {
    screen = "left";
  }
}
