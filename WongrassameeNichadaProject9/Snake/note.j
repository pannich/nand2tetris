class Snake {
  field Array segments; // Array of Point objects representing the snake's body
  field int direction; // The current direction of the snake
  field int length; // Current length of the snake


  constructor Snake new(int startX, int startY, int startLength) {
    var int i;
    var Point temp;

    let length = startLength;
    let segments = Array.new(length);
    let direction = 0; // Assume 0=right, 1=down, 2=left, 3=up as direction codes

    // Initialize snake segments to start positions

    let i = 0;

    while( i < length ) {
      // let temp = Point.new(0,0);
      // do temp.setX(startX - i);
      // do temp.setY(startY);
      // let segments[i] = temp;
      let i = i + 1;
    }


    // do draw();

    return this; // Return a reference to this newly created object
    }



  /** Draw snake in its current (x,y) location */
  method void draw() {
    var int i, segX, segY;
    var Point temp;

    // Draws the pixel using the color black
    do Screen.setColor(true);

    let i = 0;
    // Iterate through each segment of the snake and draw it
    while( i < length ) {
      let temp = segments[i];
      let segX = temp.getX();
      let segY = temp.getY();
      do Screen.drawPixel(segX, segY);
      let i = i + 1;
    }
    return;
  }

  method void move() {
    var int i;
    var Point temp, prev;

    // Move head in the current direction
    let temp = segments[0];
    if (direction = 0) { do temp.setX(temp.getX() + 1); } // Right
    if (direction = 1) { do temp.setY(temp.getY() + 1); } // Down
    if (direction = 2) { do temp.setX(temp.getX() - 1); } // Left
    if (direction = 3) { do temp.setY(temp.getY() - 1); } // Up

    // Move the rest of the body by one
    let i = 0;
    while (i < length) {
        let prev = segments[i];
        let segments[i] = temp;
        let temp = prev;
        let i = i + 1;
    }
    return;
  }

  method void changeDirection(int newDirection) {
    // Prevent newDirection pointing to the snake itself
    // check valid move
    if ((newDirection - direction = 2) | (direction - newDirection = 2)) {
      return;
    }
      else {
        let direction = newDirection;
      }
    return;
  }

  method void grow() {
    var Array newSegments;
    var int i;
    // Allocate a new longer Array
    let newSegments = Array.new(length + 1);

    // Copy over the existing segments
    let i = 0;
    while (i < length) {
      let newSegments[i] = segments[i];
      let i = i + 1;
    }

    let length = length + 1 // Increment the length of the new snake
    // calculate new position TODO : Recheck ?? Now is overlapping the previous tail

    // Move tail in the current direction
    let newX = segments[length - 2].getX();
    let newY = segments[length - 2].getY();

    if (direction = 0) { let newX = newX - 1; } // Move Right, add tail to left
    if (direction = 1) { let newY = newY - 1; } // Moving Down, add new segment above
    if (direction = 2) { let newX = newX + 1; } // Moving Left, add new segment to the right
    if (direction = 3) { let newY = newY + 1; } // Moving Up, add new segment below

    let newSegments[length - 1] = Point.new(newX, newY);

    // Replace the old segments array with the new, larger array
    let segments = newSegments;
    return;
  }

  method boolean checkCollision() {
    var int i;
    var Point head;
    let head = segments[0];

    // Check for self-collision. If head overlap with any part of the body.
    for (i = 1; i < length; i = i + 1) {
        if ((head.getX() = segments[i].getX()) & (head.getY() = segments[i].getY())) {
            return true; // Collision detected
        }
    }
    // Add boundary collision checks here
    for (i = 1; i < length; i = i + 1) {
        if ((segments[i].getX()<0) | (segments[i].getY()<0) | (segments[i].getX()>511) | (segments[i].getY()>255) <0) {
          return true; // Collision detected
        }
    }

    return false; // No collision
  }

}



// draws the current head of the snake
  method void drawHead(int cycle) {
      do Screen.setColor(true);
      do Screen.drawPixel(currX, currY);

      let histX[cycle] = currX;
      let histY[cycle] = currY;

      return;

  }

  // Remove previous Tail
  method void clearTail(int cycle) {
      var int tailPos, tailX, tailY;

      let tailIndex = cycle - length;
      let tailX = histX[tailPos];
      let tailY = histY[tailPos];

      // Set color to white to erase the last segment's previous position
      do Screen.setColor(false);
      do Screen.drawPixel(tailX, tailY); // prevTailX and prevTailY need to be the X and Y of the last segment before it moved

      return;
    }


// rewrites the snake's history
  method void rewriteHistory() {
      var int i, src, dst;

      let i = length;
      let dst = 0;
      let src = histSize - length;  // copy the last snake over to the new array
      while( i > 0 ) {
          let histX[dst] = histX[src];
          let histY[dst] = histY[src];
          let src = src + 1;
          let dst = dst + 1;
          let i = i - 1;
      }

      return;

    }


// check if the snake's history needs to be rewritten
        if( snake.checkRewriteHistory() ) {
            let cycle = snake.getLength();
        }


/** disposes of a Snake */
  method void dispose() {

      do histX.dispose();
      do histY.dispose();
      do Memory.deAlloc(this);
      return;

  }


-------------Apple
// var boolean spaceFree;
// check don't place food on the snake
    let spaceFree = false;
    while (~spaceFree){
      if( ~ checkOccupied(apple.getAppleX(), apple.getAppleY()) ) {   // if not occupied go place the apple
        let spaceFree = true;
        }
    }
