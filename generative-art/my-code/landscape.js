// dimensions
let screenHeight = 766;
let screenWidth = 4078;
let numScreens = 6;
let blocks = []

// parameters
let t = 0;
// let fr = 60;
let numWaves = 3;
const waveValues = new Array(Math.floor(screenHeight / numWaves));
const oceanColors = ["#074a53", "#077395", "#5b9299", "#8dc1cf", "#aadbe1", "#b8bec0"];
const sandColors = ["#f6d7b0", "#f2d2a9", "#eccca2", "#e7c496", "#e1bf92"]
const sandValues = new Array(20);
let sand = null;
const numUmbrellas = 40;
let umbrellaColors = new Array(numUmbrellas).fill(null);
let umbrellaLocations = new Array(numUmbrellas).fill(null);

const waveColors = [];
let theta = 0;

function setup() {
  createCanvas(screenWidth, screenHeight);
  noFill();
  // frameRate(fr);
  dx = (TWO_PI / 500.0) * 3; 
  for (let i = blocks[5]; i < blocks[5] + 2 * screenWidth / numScreens; i += 20) {
    waveColors.add(oceanColors[round(random(oceanColors.length - 1))]);
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

  for (let block = 0; block < 2; block += 1) {
    for (let i = blocks[block] + 300; i < blocks[block] + 750; i += 100) {
      strokeWeight(20);
      if (t % 10 == 0) {
        waveColors[i - blocks[block]] = oceanColors[round(random(oceanColors.length - 1))];
      }
      stroke(waveColors[i - blocks[block]]);
      calcWave();
      renderWave(i);
      coverBlock(block + 1);
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
    rotate(frameCount / 50.0);
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
  for (let i = 0; i < waveValues.length; i++) {
    waveValues[i] = sin(y) * 75;
    y += dx;
  }
}

function rotate() {

}

function renderWave(translateX) {
  for (let x = 0; x < waveValues.length; x++) {
    ellipse(translateX + waveValues[x], x * numWaves, 40, 40);
  }

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
    console.log(this.x);
    console.log(this.y);
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
  rect(blocks[block], 0, screenWidth / numScreens, screenHeight);
}