'''
VMWriter

Nichada Wongrassamee
'''

class VMWriter:
    """write .jack to .vm files
    """
    segment_dict = {
        "CONST" : "constant",
        "ARG" : "argument",
        "LOCAL" : "local",
        "STATIC" : "static",
        "THIS" : "this",
        "THAT" : "that",
        "POINTER" : "pointer",
        "TEMP" : "temp"
    }

    def __init__(self, output_file):
        """Creates a new file and prepares it for writing VM commands
        """
        self.output = open(output_file, 'w')    # TODO don't forget to close


    def writePush(self, segment, index):
        """
        Writes a VM push command
        Segment (CONST, ARG, LOCAL, STATIC, THIS, THAT, POINTER, TEMP)
        Index (int)

        ie. 'push const 1'
        """
        self.output.write(f'push {self.segment_dict[segment]} {index}\n')

    def writePop(self, segment, index):
        """
        Writes a VM pop command
        Segment (CONST, ARG, LOCAL, STATIC, THIS, THAT, POINTER, TEMP)
        Index (int)
        """
        self.output.write(f'pop {self.segment_dict[segment]} {index}\n')

    def writeArithmetic(self, command):
        """
        command (ADD, SUB, NEG, EQ, GT, LT, AND, OR, NOT)
        """
        self.output.write(command.lower() + '\n')

    def writeLabel(self, label):
        """ Writes a VM label command """
        self.output.write(f'label {label}\n')

    def writeGoto(self, label):
        self.output.write(f'goto {label}\n')

    def writeIf(self, label):
        """ Writes a VM If-goto command """
        self.output.write(f'if-goto {label}\n')

    def writeCall(self, name, nArgs):
        """ Writes a VM call command
        name (String)
        nArgs (int)
        """
        self.output.write(f'call {name} {nArgs}\n')

    def writeFunction(self, name, nLocals):
        """ Writes a VM function command
        name (String)
        nLocals (int)
        """
        self.output.write(f'function {name} {nLocals}\n')

    def writeReturn(self):
        self.output.write('return\n')

    def close(self):
        self.output.close()
