=== README.txt ===

## Description
Project04 involves implementing assembly language scripts

All working scripts:

1. Mult.asm
: this program multiplies the values found in memory location 0 (R0) and memory location 1 (R1)
and stores the result in memory location 2 (R2). For the purpose of this program, we assume that R0>=0, R1>=0,
and R0*R1<32768 (you are welcome to ponder where this value comes from).
our program need not test these conditions, but rather assume that they hold.
To test your program, put some values in RAM[0] and RAM[1], run the code, and inspect RAM[2].
The supplied Mult.tst script and Mult.cmp compare file are deigned to test your program "officially"
, running it on several representative values supplied by the test script.

2. Fill.asm
: This program illustrates low-level handling of the screen and keyboard devices.
In particulate, the program runs an infinite loop that listens to the keyboard input.
When a key is pressed (any key), the program blackens the screen, i.e. writes "black" in every pixel.
When no key is pressed, the program clears the screen, i.e. writes "white" in every pixel.
The white must fill in backwards, starting at the end of the black section.
Pressing a key continuously for long enough should result in a fully blackened screen, and not pressing
any key for long enough should result in a fully cleared screen.
A test script (Fill.tst) is provided in the Project 4 folder, but no compare file.
The program should be checked visually by inspecting the screen of the CPU Emulator.
