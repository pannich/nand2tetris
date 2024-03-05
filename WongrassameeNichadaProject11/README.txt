=== README.txt ===

Instructions for Compilation:
- Use Python 3.10.9.

Instructions for Running the Code:
- Enter scr
- Run `python JackCompiler.py <jack_file_directory or filepath.jack>`

Functionality:

- Compile jack instruction to VM code

Modules:
- A main driver that organizes and invokes everything (JackCompiler);
- A tokenizer (JackTokenizer);
- A symbol table (SymbolTable);
- An output module for generating VM commands (VMWriter);
- A recursive top-down compilation engine (CompilationEngine).

[List any known limitations or issues.]
- none

=== End of README.txt ===
