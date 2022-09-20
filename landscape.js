// dimensions
let screenHeight = 766;
let screenWidth = 4078 / 2;
let numScreens = 3;
let blocks = []

// parameters
let t = 0;
let fr = 20;
let numWaves = 3;
const waveValues = new Array(Math.floor(screenHeight / numWaves) * 2);
const oceanColors = ["#074a53", "#077395", "#5b9299", "#8dc1cf", "#aadbe1", "#b8bec0"];
const sandColors = ["#f6d7b0", "#f2d2a9", "#eccca2", "#e7c496", "#e1bf92"]
const sandValues = new Array(20);
let sand = null;
const numUmbrellas = 40;
let umbrellaColors = new Array(numUmbrellas).fill(null);
let umbrellaLocations = new Array(numUmbrellas).fill(null);
let screen = "left";

const waveColors = new Array(20);
let theta = 0;

function setup() {
  createCanvas(screenWidth, screenHeight);
  noFill();
  frameRate(20);
  dx = (TWO_PI / 500.0) * 3; 
  for (let i = 0; i < 20; i ++) {
    waveColors[i] = oceanColors[round(random(oceanColors.length - 1))];
  }
  sand = sandColors[floor(random(5))];
  background(sand);
}

function draw() {

  stroke('black');
  strokeWeight(1);
  fill(sand);
  background(sand);
  createScreenSplits();

  if (screen == "left") {
    // for (let block = 0; block < 2; block += 1) {
      waveCount = 0;
      for (let i = blocks[0] + 500; i < blocks[0] + 800; i += 80) {
        strokeWeight(10);
        if (t % 10 == 0) {
          waveColors[waveCount] = oceanColors[round(random(oceanColors.length - 1))];
        }
        fill(waveColors[waveCount]);
        stroke(waveColors[waveCount]);
        calcWave();
        renderWave(i, 1, 2);
        waveCount++;
      }

      noFill();
      strokeWeight(20);
      stroke('black');
      curve(screenWidth, 50, screenWidth - 10, screenHeight, screenWidth - (screenWidth / numScreens / 2) + 50, 0, 200, 200);
      stroke(0);
      curve(5, 26, 0, 73, 24, 0, 73, 61, 0, 15, 65, 0);
      stroke(255, 102, 0);
      curve(73, 24, 0, 73, 61, 0, 15, 65, 0, 15, 65, 0);
    // }
  } else {
    waveCount = 0;
    for (let i = blocks[1] + 500; i < blocks[1] + 800; i += 80) {
      strokeWeight(10);
      if (t % 10 == 0) {
        waveColors[waveCount] = oceanColors[round(random(oceanColors.length - 1))];
      }
      fill(waveColors[waveCount]);
      stroke(waveColors[waveCount]);
      calcWave();
      renderWave(i, 2, 2);
      waveCount++;
    }
  }

  for (let i = 0; i < umbrellaColors.length; i++) {
    if (umbrellaColors[i] == null) {
      umbrellaColors[i] = color(floor(random(255)), floor(random(255)), floor(random(255)));
    }

    if (umbrellaLocations[i] == null) {
      umbrellaLocations[i] = [random(1), random(1)];
    }
    fill(umbrellaColors[i]);
    strokeWeight(0);

    push();
    translate(width * umbrellaLocations[i][0], height * umbrellaLocations[i][1]);
    rotate(frameCount / 30.0);
    polygon(0, 0, 50, 8);
    pop();

    stroke("black");
    strokeWeight(10);

    push();
    translate(width * umbrellaLocations[i][0], height * umbrellaLocations[i][1]);
    ellipse(0, 0, 1, 1);
    pop();
  }

  // frameRate(fr);
  t++;
}

function createScreenSplits() {
  for (let i = 0; i < numScreens; i++) {
    rect(screenWidth / numScreens * i, 0, screenWidth / numScreens, screenHeight);
    blocks.push(screenWidth / numScreens * i);
  }
}

function calcWave() {
  theta += 0.02;
  let y = theta;
  for (let i = 0; i < waveValues.length / 2; i++) {
    waveValues[i] = sin(y) * 75;
    y += dx;
  }
  y += 10;
  for (let i = waveValues.length / 2; i < waveValues.length; i++) {
    waveValues[i] = screenWidth / numScreens + sin(y) * 75;
    y += dx;
  }
}

function rotate() {

}

function renderWave(translateX, block1, block2) {
  for (let x = 0; x < waveValues.length / 2; x++) {
    ellipse(translateX + waveValues[x], x * numWaves, 40, 40);
  }
  coverBlock(block1);
  strokeWeight(10);

  for (let x = 0; x < waveValues.length / 2; x++) {
    ellipse(translateX + waveValues[waveValues.length / 2 + x], x * numWaves, 40, 40);
  }
  coverBlock(block2);

  // for (let x = 0; x < waveValues.length; x++) {
  //   ellipse(translateX * 2 + waveValues[x], x * numWaves, 40, 40);
  // }
}

class Umbrella {
  constructor(x, y) {
    this.x = x;
    this.y = y;
    this.color = null;
  }

  create() {
    this.color = color(floor(random(255)), floor(random(255)), floor(random(255)));
  }

  update() {
    strokeWeight(0);
    stroke(this.color);
    fill(this.color);

    strokeWeight(10);
    stroke('black');
    ellipse(this.x + 20, this.y + 20, 50, 50);
  }
}

function polygon(x, y, radius, npoints) {
  let angle = TWO_PI / npoints;
  beginShape();
  for (let a = 0; a < TWO_PI; a += angle) {
    let sx = x + cos(a) * radius;
    let sy = y + sin(a) * radius;
    vertex(sx, sy);
  }
  endShape(CLOSE);
}

function coverBlock(block) {
  strokeWeight(0);
  fill(sand);
  rect(blocks[block], 0, screenWidth / numScreens / 2, screenHeight);
}

function keyPressed() {
  if (keyCode == ENTER) {
    screen = "right";
  } else if (keyCode == BACKSPACE) {
    screen = "left";
  }
}