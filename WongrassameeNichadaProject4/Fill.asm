// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen
// by writing 'black' in every pixel;
// the screen should remain fully black as long as the key is pressed.
// When no key is pressed, the program clears the screen by writing
// 'white' in every pixel;
// the screen should remain fully clear as long as no key is pressed.

//// Replace this comment with your code.

// white = 00...00
// black = 11...11 = -1
// @SCREEN = start of screen
// @KBD = not 0 when key pressed

// Set up
@SCREEN
D=A
@i
M=D // M[i] = current screen location

(ISKBD)
@KBD
D=M // D=KBD
@BLACKEN
D;JGT // KBD > 0 go to Fill Black
@WHITEN
D;JEQ // KBD == 0 go to Fill White

(BLACKEN)
@i
A=M
M=-1 // Fill black
D=A // D = current location
@KBD
A=A-1
D=D-A // D = i - KBD - 1
@ISKBD
D;JEQ // Go back if D==0 . At end of screen.
@i
M=M+1 // Else inc i
@ISKBD
0;JMP

(WHITEN)
@i
A=M
M=0 // Fill white
D=A // D = current location bc. D=A=M[i]
@SCREEN
D=D-A // D = i - SCREEN
@ISKBD
D;JLE // Reset i if D<0 . Beyond start of screen.
@i
M=M-1
@ISKBD
0;JMP
