// dimensions
let screenHeight = 766;
let screenWidth = 4078;
let numScreens = 6;
let blocks = []

// parameters
let t = 0;
let fr = 20;
let numWaves = 3;
const waveValues = new Array(Math.floor(screenHeight / numWaves));
const oceanColors = ["#074a53", "#077395", "#5b9299", "#8dc1cf", "#aadbe1", "#b8bec0"];

const waveColors = [];
let theta = 0;

function setup() {
  createCanvas(screenWidth, screenHeight);
  background(oceanColors[0]);
  noFill();
  frameRate(fr);
  dx = (TWO_PI / 500.0) * 3; 
  for (let i = blocks[5]; i < blocks[5] + 2 * screenWidth / numScreens; i += 20) {
    waveColors.add(oceanColors[round(random(oceanColors.length - 1))]);
  }
}

function draw() {
  stroke('black');
  strokeWeight(1);
  background(51);
  createScreenSplits();
  calcWave();
  renderWave(blocks[1]);

  strokeWeight(20);
  for (let i = blocks[5]; i < blocks[5] + 2 * screenWidth / numScreens; i += 20) {
    if (t % 5 == 0) {
      waveColors[i - blocks[5]] = oceanColors[round(random(oceanColors.length - 1))];
    }
    stroke(waveColors[i - blocks[5]]);
    calcWave();
    renderWave(i);
  }

  frameRate(fr);
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
  for (let i = 0; i < waveValues.length; i++) {
    waveValues[i] = sin(y) * 75;
    y += dx;
  }
}

function rotate() {

}

function renderWave(translateX) {
  for (let x = 0; x < waveValues.length; x++) {
    ellipse(translateX + waveValues[x], x * numWaves, 16, 16);
  }
}