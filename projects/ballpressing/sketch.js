let targets = [];
let score = 0;
let gameState = 'START'; 
let timer = 60;
let lastSpawnTime = 0;
let spawnRate = 1000;
let lives = 3;

function setup() {
  createCanvas(windowWidth, windowHeight);
  textAlign(CENTER, CENTER);
  textFont('sans-serif');
}

function draw() {
  background(20);

  if (gameState === 'START') {
    drawMenu("TAP TO START", "Clear circles before they grow too large.");
  } else if (gameState === 'PLAY') {
    handlePlayState();
  } else if (gameState === 'GAMEOVER') {
    drawMenu("GAME OVER", "Score: " + score + "\nTap to Restart");
  }
}

function handlePlayState() {
  updateTimer();
  manageSpawns();
  updateTargets();
  drawUI();

  if (timer <= 0 || lives <= 0) {
    gameState = 'GAMEOVER';
  }
}

function updateTimer() {
  if (frameCount % 60 === 0 && timer > 0) {
    timer--;
  }
}

function manageSpawns() {
  let now = millis();
  if (now - lastSpawnTime > spawnRate) {
    spawnTarget();
    lastSpawnTime = now;
    spawnRate = max(300, spawnRate * 0.98);
  }
}

function spawnTarget() {
  let r = random(30, 60);
  let x = random(r, width - r);
  let y = random(r, height - r);
  targets.push({ x, y, size: r, maxS: random(150, 250), growth: random(1, 3) });
}

function updateTargets() {
  for (let i = targets.length - 1; i >= 0; i--) {
    let t = targets[i];
    t.size += t.growth;

    // Blue fill update
    fill(0, 120, 255, 150);
    stroke(255);
    strokeWeight(2);
    ellipse(t.x, t.y, t.size);

    if (t.size > t.maxS) {
      targets.splice(i, 1);
      lives--;
    }
  }
}

function drawUI() {
  fill(255);
  noStroke();
  textSize(24);
  text("Time: " + timer, width * 0.2, 40);
  text("Score: " + score, width * 0.5, 40);
  text("Lives: " + lives, width * 0.8, 40);
}

function drawMenu(title, subtitle) {
  fill(255);
  textSize(40);
  text(title, width / 2, height / 2 - 20);
  textSize(18);
  text(subtitle, width / 2, height / 2 + 30);
}

function touchStarted() {
  if (gameState === 'START' || gameState === 'GAMEOVER') {
    resetGame();
    return false;
  }

  if (gameState === 'PLAY') {
    let hit = false;
    for (let i = targets.length - 1; i >= 0; i--) {
      let t = targets[i];
      let d = dist(mouseX, mouseY, t.x, t.y);
      if (d < t.size / 2 + 20) {
        targets.splice(i, 1);
        score++;
        hit = true;
        break;
      }
    }
  }
  return false;
}

function resetGame() {
  targets = [];
  score = 0;
  timer = 60;
  lives = 3;
  spawnRate = 1000;
  gameState = 'PLAY';
}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
}
