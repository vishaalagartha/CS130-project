var dict = {
  Lorem:1,
  ipsum:2,
  dolor:3,
  sit:4,
  amet:5,
  consectetur:6,
  adipiscing:7,
  elit:8, 
  sed:9,
  do:10
}

var scalar = 0.82; // Different for each font
var debug = false;

var font,
    fontSize = 80,
    minFontSize = 12;

var spring = 0.5;
var force = 10000;
  
var x,y, cloud;

class wordCloud {
  constructor(wordDict) {
    this.wordDict = wordDict;
    this.wordBoxes = [];
    var maxFreq = 0;
    for (const [word, freq] of Object.entries(wordDict)) {
      if (freq > maxFreq) {
        maxFreq = freq;
      }
    }
    for (const [word, freq] of Object.entries(wordDict)) {
      this.wordBoxes.push(new wordBox(word, freq, maxFreq));
    }
  }

  render() {
    for (var i = 0; i < this.wordBoxes.length; i++) {
      this.wordBoxes[i].render();
    }
  }

  handleCollisions() {
    for (var i = 0; i < this.wordBoxes.length; i++) {
      for (var j = 0; j < this.wordBoxes.length; j++) {
        if (i == j) continue;
        // console.log(this.wordBoxes[i], this.wordBoxes[j]);
        this.wordBoxes[i].handleCollision(this.wordBoxes[j]);
        this.wordBoxes[i].move();
      }
    }
  }
}

class wordBox {
  constructor(text, freq, maxFreq) {
    this.text = text;
    this.freq = freq;
    this.maxFreq = maxFreq;
    this.fontSize = map(freq/maxFreq, 0, 1, minFontSize, fontSize);
    textSize(this.fontSize);
    this.rect = new Rectangle(width / 2, height / 2, textWidth(text), this.fontSize);
    this.yOffset = this.fontSize * (1 - scalar);
  }

  render() {
    textSize(this.fontSize);
    text(this.text, this.rect.x, this.rect.y - this.yOffset);
    if (debug) {
      this.rect.render();
    }
  }
  
  handleCollision(other) {
    this.rect.handleCollision(other.rect);
  }

  move() {
    this.rect.move();
  }
}

class Rectangle {
  constructor(x,y,w,h) {
    this.x = x;
    this.y = y;
    this.w = w;
    this.h = h;
    this.midX = x + w / 2;
    this.midY = y + h / 2;
    this.vx = 0;
    this.vy = 0;
  }

  area() {
    return this.w * this.h;
  }

  render() {
    rect(this.x, this.y, this.w, this.h);
  }

  handleCollision(other) {
    if (!this.collides(other)) {
      // console.log('no collision');
      return
    }
    // console.log("here");
    var dx = this.midX - other.midX,
        dy = this.midY - other.midY;
    if (dx < 0.5 && dx >= 0) {
      dx = 0.5;
    } else if (dx > -0.5 && dx <= 0) {
      dx = -0.5;
    }
    if (dy < 0.5 && dy >= 0) {
      dy = 0.5;
    } else if (dy > -0.5 && dy <= 0) {
      dy = -0.5;
    }
    var distance = sqrt(dx * dx + dy * dy);

    var dxn = dx / distance,
        dyn = dy / distance;
    // console.log(dx, dy);
    this.vx += force * spring / pow(this.area(), 0.3) * dx / distance / distance;
    this.vy += force * spring / pow(this.area(), 0.3) * dy / distance / distance;
  }

  move() {
    this.x += this.vx;
    this.y += this.vy;
    this.midX = this.x + this.w / 2;
    this.midY = this.y + this.h / 2;
    this.vx = 0;
    this.vy = 0;
  }

  collides(other) {
    if (this.x < other.x + other.w && this.x + this.w > other.x &&
          this.y < other.y + other.h && this.y + this.h > other.y) {
      return true;
    }
    return false;
  }
}

function setup() {
  createCanvas(720, 400);
  textSize(fontSize);
  textAlign(LEFT, TOP);
  textLeading(0);
  x=new wordBox("pooE", 5, 10);
  y=new wordBox("eggs", 10, 10);
  cloud = new wordCloud(dict);
}


function draw() {
  if (debug) {
    noFill();
    stroke(255, 128, 0);
  } else {

  }
  background(255);

  cloud.handleCollisions();
  cloud.render();
}