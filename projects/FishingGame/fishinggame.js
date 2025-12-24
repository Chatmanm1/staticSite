let fishTable = [
  { name: "Old Boot", value: 1, weight: 1 },
  { name: "Minnow", value: 5, weight: 3 },
  { name: "Trout", value: 10, weight: 6 },
  { name: "Salmon", value: 18, weight: 10 },
  { name: "Golden Carp", value: 40, weight: 2 },
  { name: "Legendary Leviathan", value: 100, weight: 1 },
];

let money = 0;
let rodLevel = 1;
let streak = 0;

let state = "idle"; // idle, waiting, hooked, result
let hookTime = 0;
let message = "Click CAST to fish";

let missAnim = false;
let missX, missY;
let missTimer = 0;

function setup() {
  createCanvas(500, 300);
  textAlign(CENTER, CENTER);
  textSize(16);
}
function drawMissFish(x, y) {
  push();
  translate(x, y);
  noStroke();
  fill(255, 100, 100);

  // body
  ellipse(0, 0, 30, 15);

  // tail
  fill(255, 50, 50);
  triangle(-15, 0, -25, -7, -25, 7);

  // optional eye
  fill(0);
  ellipse(8, -2, 3, 3);

  pop();
}
function draw() {
  background(30);

  fill(255);
  text(message, width / 2, 50);
  text(`Money: $${money}`, width / 2, 100);
  text(`Rod: ${rodLevel}   Streak: ${streak}`, width / 2, 130);

  drawButton();
if (missAnim) {
  drawMissFish(missX, missY);
  missY -= 5;
  missTimer -= deltaTime;
  if (missTimer <= 0) {
    missAnim = false;
  }
}
   
}

function drawButton() {
  fill(80);
  rectMode(CENTER);
  rect(width / 2, 220, 140, 50, 8);
  fill(255);

  if (state === "idle") text("CAST", width / 2, 220);
  else if (state === "hooked") text("REEL", width / 2, 220);
  else text("WAIT", width / 2, 220);
}

function mousePressed() {
  if (mouseY < 195 || mouseY > 245) return;

  if (state === "idle") {
    state = "waiting";
    message = "Casting...";
    setTimeout(() => {
      state = "hooked";
      hookTime = millis();
      message = "Fish on the line!";
    }, random(600, 1500));
  }

  else if (state === "hooked") {
    let reaction = millis() - hookTime;
    let luck = 0;

    if (reaction < 300) {
      luck = 1;
      message = "Perfect timing.";
    } else if (reaction < 800) {
      luck = 0;
      message = "Good reel.";
    } else {
      luck = -1;
      message = "Sloppy reel.";
    }

    // 66% chance to catch
    if (random() < 0.66) {
      resolveCatch(luck);
    } else {
      message = "The fish got away!";
      streak = 0;  // reset streak
      state = "idle";

      // trigger miss animation
      missAnim = true;
      missX = width / 2;
      missY = 180;
      missTimer = 500; // milliseconds
    }
  }
}

function resolveCatch(luck) {
  let pool = [];

  fishTable.forEach(f => {
    let adjusted = max(1, f.weight + luck);
    for (let i = 0; i < adjusted * rodLevel; i++) {
      pool.push(f);
    }
  });

  let fish = random(pool);
  streak++;

  let bonus = floor(streak / 5);
  let payout = fish.value + bonus;
  money += payout;

  message = `Caught ${fish.name} (+$${payout})`;

  if (random() < 0.15) {
    streak = 0;
    message += " — Line snapped.";
  }

  state = "idle";
}

