# VM translator
#
# Nichada Wongrassamee

from program0 import parseempty
import sys
import os

class Parser:
    """
    parse <filein>.vm into <fileout>.out

    Args:
        filein (str.vm): input file
        fileout (str): <filepath>.out
    """

    def __init__(self, arg) -> None:
        self.arg = arg
        self.ext = ".vm"
        self.filename_no_ext = self.extract_filename()
        self.in_file = f'{self.filename_no_ext}.vm'
        self.out_file = f'{self.filename_no_ext}.out'

    def extract_filename(self):
        """
        check if input file is .ext file

        Return:
            None if file not valid
            filename if file has valid extension
        """
        try:
            l_ = len(self.ext)
            filename_no_ext = self.arg[:-l_]  # parse filename wihtout extension
            extension = self.arg[(-l_):]
            if extension != self.ext:
                raise ValueError("File is not a .{self.ext} input")
        except ValueError as e:
            print(f"Error: {e}")
            return None
        return filename_no_ext

    def parse_comment(self):
        with open(f"{self.out_file}", "w") as fout:
            with open(f"{self.in_file}", "r") as fd:
                comment = False  # comment status at the beginning of the file
                for line in fd:
                    linenospace, comment = parseempty(line, comment)
                    if linenospace and linenospace != "\n":
                        # write to output file
                        fout.write(linenospace)
        return self.out_file

class WriteASM:
    """generate the asm commands from vm insturctions

    Raises:
        ValueError: unknown command
    """
    arguments = {
        "argument" : "ARG",
        "local" : "LCL",
        "this" : "THIS",
        "that" : "THAT",
    }

    operations = ["add", "sub", "neg", "eq", "gt" ,"lt", "and", "or", "not"]

    def __init__(self, in_file):
        self.asm = ""
        self.bool_count = 0
        self.filename_no_ext = in_file.split("/")[-1].replace(".out","")

    def set_address_A(self, args):
        # set A
        arg1, arg2, arg3 = args # push/pop segment index
        if arg2 == "constant":
            self.asm += f'@{arg3}\n'

        elif arg2 == "static":
            self.asm += "@" + self.filename_no_ext + "." + arg3 + '\n'

        elif arg2 == "temp":
            self.asm += '@' + str(5+int(arg3)) + '\n'

        elif arg2 == "pointer" and arg3 == "0":
            self.asm += '@THIS\n'
        elif arg2 == "pointer" and arg3 == "1":
            self.asm += '@THAT\n'

        elif arg2 in self.arguments: # local , argument, this, that
            self.asm += f'@{self.arguments[arg2]}\n'

    def push_command(self, args):
        """push to stack

        Push constant, D = value to push
        """
        arg1, arg2, arg3 = args # push/pop segment index

        # Get Constant D
        if arg2 == "constant":
            self.set_address_A(args)
            self.asm += 'D=A\n'
        elif arg2 in ["static", "temp", "pointer"]:
            self.set_address_A(args)
            self.asm += 'D=M\n'
        elif arg2 in self.arguments: # local , argument, this, that
            self.set_address_A(args)
            self.asm += 'D=M\n' # D=seg_address
            self.asm += f'@{arg3}\n'
            self.asm += 'A=A+D\n' # A=target address
            self.asm += 'D=M\n' # grab D from target
        else:
            self.raise_unknown(arg2)

        # Push Constant D : Set pointer to next and Set A to stack
        self.asm += "@SP\n"
        self.asm += "AM=M+1\n"
        self.asm += "A=A-1\n"
        self.asm += "M=D\n" # M[A] = D

    def pop_command(self, args):
        """pop from stack

        Pop from the top of stack and save in D
        Push D to target Address
        """
        arg1, arg2, arg3 = args

        # set target address A, pop const to D
        if arg2 in self.arguments:
            self.set_address_A(args)
            self.asm += 'D=M\n' # D=seg_address
            self.asm += f'@{arg3}\n'
            self.asm += 'D=A+D\n' # D=target address

            self.asm += '@R13\n'
            self.asm += 'M=D\n' # save target address to R13

            self.pop_to_D() # D = M[A]

            self.asm += '@R13\n'
            self.asm += 'A=M\n'

        elif arg2 in ["static", "temp", "pointer"]:
            self.pop_to_D() # D = M[A]
            self.set_address_A(args)

        else:
            self.raise_unknown(arg2)

        # finally, push D to target
        self.asm += 'M=D\n'

    def pop_to_D(self):
        """set SP and pop top of stack to D
        """
        self.asm += "@SP\n"
        self.asm += "AM=M-1\n"
        self.asm += "D=M\n"

    def set_A_to_stack(self):
        """set A to stack if not "neg", "not"
        """
        self.asm += "A=A-1\n"

    def operation(self, oper):
        """M[A] from top of stack ie @403
           D=The number previous top of stack ie @404
           SP points to the next available spot ie @404

        Args:
            oper (_type_): add, sub, neg, eq, gt ,lt, and, or, not
        """
        if oper == "add":
            self.asm += "M=M+D\n"
        elif oper == "sub":
            self.asm += "M=M-D\n"
        elif oper in ["eq", "gt" ,"lt"]: # boolean operation
            self.asm += "D=M-D\n" # D = M[A] - D
            self.asm += "M=-1\n" # Set to True first
            self.asm += f"@CONTINUE{self.bool_count}\n"

            # CONTINUE if TRUE
            if oper == "eq":
                self.asm += "D;JEQ\n"
            elif oper == "gt":
                self.asm += "D;JGT\n" # True when M[A] > D
            elif oper == "lt":
                self.asm += "D;JLT\n" # True when M[A] < D

            # Else change to FALSE
            self.asm += "@SP\n"
            self.asm += "A=M-1\n" # ie. A=403
            self.asm += "M=0\n"

            self.asm += f"(CONTINUE{self.bool_count})\n"
            self.bool_count+=1

        elif oper == "and":
            self.asm += "M=D&M\n"
        elif oper == "or":
            self.asm += "M=D|M\n"

        elif oper in ["neg", "not"]:
            if oper == "neg":
                self.asm += "M=-M\n"
            elif oper == "not":
                self.asm += "M=!M\n"

            # increment SP to 405
            self.asm += "@SP\n"
            self.asm += "M=M+1\n"
        else:
            self.raise_unknown(oper)

    def raise_unknown(self, argument):
        raise ValueError('{} is an invalid argument'.format(argument))

class Translator:
    """tramslate <filename>.out to <filename>.asm
    """
    def __init__(self, in_file, out_file):
        self.WriteASM = WriteASM(in_file)
        self.in_file = in_file
        self.out_file = out_file

    def main(self):
        with open(f"{self.out_file}", "w") as fout:
            with open(f"{self.in_file}", "r") as fd:
                for line in fd:
                    instructions = line.split()
                    arg1 = instructions[0]
                    if arg1 == "push":
                        self.WriteASM.push_command(instructions)
                    elif arg1 == "pop":
                        self.WriteASM.pop_command(instructions)
                    elif arg1 in self.WriteASM.operations: # arithmetic command
                        self.WriteASM.pop_to_D()
                        if arg1 not in ["not", "neg"]:
                            self.WriteASM.set_A_to_stack()
                        self.WriteASM.operation(arg1)
            fout.write(self.WriteASM.asm)
        return

def main():
    parser = Parser(sys.argv[1])
    filename_no_ext = parser.filename_no_ext
    if filename_no_ext is None:
        return
    file_parsed_comment = parser.parse_comment() # <filename>.out

    translator = Translator(file_parsed_comment, f"{filename_no_ext}.asm")
    translator.main()

    #clean up
    os.remove(f"{filename_no_ext}.out")

if __name__ == "__main__":
    main()
