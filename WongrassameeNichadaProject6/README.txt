=== README.txt ===

Instructions for Compilation:
- Use Python 3.10.9.

Instructions for Running the Code:
- Run `python src/assembly.py <filepath>.asm` ie. python src/assembly.py rect/Rect.asm

Assembler Functionality:
- Change assembly code(.asm) into machine code (.hack)

- Pass 1 :
  Use parser.py to remove comments and empty spaces.
  Remove all comments. Comments come in two forms:
• comments can begin with the sequence "//" and end at the line return
• comments can begin with the sequence /* and end at the sequence */ (which
might be on another line)
- <filename> can be relative or absolute path

- Pass 2 :
  Save symbols '()' into symbols table.

- Pass 3 :
  Convert .asm command into 16-bit machine code from parseing A-Instruction and C-Instruction.

[List any known limitations or issues.]
- Only remove the comments in the forms described above.

=== End of README.txt ===
