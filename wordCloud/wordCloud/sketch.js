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
  do:10,
}

var scalar = 0.82; // Different for each font
var debug = false;

var font,
    fontSize = 80,
    minFontSize = 12;

var spawnBoxSize = 30;

var spring = 0.5;
var force = 500000;
  
var x,y, cloud;

class wordCloud {
  constructor(wordDict) {
    this.wordDict = wordDict;
    this.wordBoxes = [];
    /*
	    boundaries are much bigger than necessary to ensure that 
	    no words exit the screen by jumping over or through a boundary

    	(0,0)
		|--------|--------|--------|
		|        |   b3   |        |
		|        |        |        |
		|        |--------|        |
		|   b2   | canvas |   b1   |
		|        |        |        |
		|        |--------|        |
		|        |   b4   |        |
		|        |        |        |
		|--------|--------|--------|
								  (width, height)
    */
    this.boundaries = [
    	//b1
    	new Rectangle(width,  -height, width, height * 3),
    	//b2
    	new Rectangle(-width, -height, width, height * 3),
    	//b3
    	new Rectangle(0, -height, width, height),
    	//b4
    	new Rectangle(0, height, width, height)
    ];

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
    if (debug) {
    	for (var i = 0; i < this.boundaries.length; i++) {
    		this.boundaries[i].render();
    	}
    }
  }

  handleCollisions() {
    for (var i = 0; i < this.wordBoxes.length; i++) {
      for (var j = i; j < this.wordBoxes.length; j++) {
        if (i == j) continue;
        this.wordBoxes[i].handleCollision(this.wordBoxes[j]);
      }
    }
    for (var i = 0; i < this.wordBoxes.length; i++) {
    	this.wordBoxes[i].move();
    }
  }

  handleBoundary() {
  	for (var i = 0; i < this.wordBoxes.length; i++) {
		for (var j = 0; j < this.boundaries.length; j++) {
			this.wordBoxes[i].handleBoundary(this.boundaries[j]);
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
    var randX = Math.random() * 30 - 15;
    var randY = Math.random() * 30 - 15;
    this.rect = new Rectangle(width / 2 - textWidth(text) / 2 + randX, 
    						  height / 2 + randY, 
    						  textWidth(text), 
    						  this.fontSize * scalar);
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

  handleBoundary(bound) {
  	this.rect.handleCollision(bound);
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
    var dx = this.getDX(this, other),
        dy = this.getDY(this, other);
    var threshold = 1.0;
    if (dx < threshold && dx >= 0) {
      dx = threshold;
    } else if (dx > -threshold && dx <= 0) {
      dx = -threshold;
    }
    if (dy < threshold && dy >= 0) {
      dy = threshold;
    } else if (dy > -threshold && dy <= 0) {
      dy = -threshold;
    }
    var distance = sqrt(dx * dx + dy * dy);

    // var constvx = force * spring * dx / distance / distance,
    // 	constvy = force * spring * dy / distance / distance;
    var constvx = force * spring / dx / Math.pow(Math.abs(dx), 1),
    	constvy = force * spring / dy / Math.pow(Math.abs(dy), 1);

    var areaScale1 = pow(this.area(), 0.3);
    var areaScale2 = pow(other.area(), 0.3);

    var max = 1;
    this.vx += clampAbs(constvx / areaScale1, max);
    this.vy += clampAbs(constvy / areaScale1, max);
    other.vx -= clampAbs(constvx / areaScale2, max);
    other.vy -= clampAbs(constvy / areaScale2, max);
  }

  getDX(rect1, rect2) {
  	return rect1.midX - rect2.midX;
  }

  getDY(rect1, rect2) {
  	return rect1.midY - rect2.midY;
  }

  getDX2(rect1, rect2) {

  }

  getDY2(rect1, rect2) {

  }

  move() {
  	var drag = 0.3;
    this.x += this.vx;
    this.y += this.vy;
    this.midX = this.x + this.w / 2;
    this.midY = this.y + this.h / 2;
    // this.vx = 0;
    // this.vy = 0;
    this.vx = this.vx * drag;
    this.vy = this.vx * drag;
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

  cloud.handleBoundary();
  cloud.handleCollisions();
  cloud.render();
}

function clampAbs(val, max) {
	var sign = (val < 0) ? -1 : 1;
	var temp = (val < 0) ? -val : val;
	if (temp > max) {
		return sign * max;
	} else {
		return val;
	}
}