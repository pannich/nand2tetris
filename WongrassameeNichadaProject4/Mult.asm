// this program multiplies the values found in
// memory location 0 (R0) and memory location 1 (R1)
// and stores the result in memory location 2 (R2).
// For the purpose of this program, we assume that R0>=0,
// R1>=0, and R0*R1<32768 (you are welcome to ponder where
// this value comes from). Your program need not test these
// conditions, but rather assume that they hold.
// To test your program, put some values in RAM[0] and RAM[1],
// run the code, and inspect RAM[2].

// prod = mult1 * multiplier(i)

// setting
@R2
M=0  // ans = 0
@R1
D=M
@i
M=D // i=multiplier
@R0
D=M // D = mult1

(LOOP)
  @i
  M=M-1 // i--
  @END
  M;JLT // if i==0 jump to END

  @R2
  M=M+D // ans = ans + mult1
  @LOOP
  0;JMP // else back to loop

(END)
  @END
  0;JMP // INFINITE LOOP
