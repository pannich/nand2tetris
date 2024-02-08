import re

class MachineCode:
    """
    A class representing Machine Code conversion.

    Attributes:
    """
    # these variables are global to the class
    var = 16

    dest={'':'000','M=':'001','D=':'010','MD=':'011',
      'A=':'100','AM=':'101','AD=':'110','AMD=':'111'}
    jump={'':'000',';JGT':'001',';JEQ':'010',';JGE':'011',
        ';JLT':'100',';JNE':'101',';JLE':'110',';JMP':'111'}
    comp={'0':'0101010','1':'0111111','-1':'0111010','D':'0001100',
        'A':'0110000','M':'1110000','!D':'0001101','!A':'0110001',
        '!M':'1110001','-D':'0001111','-A':'0110011','-M':'1110011',
        'D+1':'0011111','A+1':'0110111','M+1':'1110111','D-1':'0001110',
        'A-1':'0110010','M-1':'1110010','D+A':'0000010','D+M':'1000010',
        'D-A':'0010011','D-M':'1010011','A-D':'0000111','M-D':'1000111',
        'D&A':'00000000','D&M':'1000000','D|A':'0010101','D|M':'1010101'}
    symbols={'SP':0,'LCL':1,'ARG':2,'THIS':3,'THAT':4,'SCREEN':16384,'KBD':24576,
            'R0':0,'R1':1,'R1':1,'R2':2,'R3':3,'R4':4,'R5':5,'R6':6,'R7':7,
            'R8':8,'R9':9,'R10':10,'R11':11,'R12':12,'R13':13,'R14':14,'R15':15}

    def __init__(self):
        pass

    def store_symbol(self, command, linenum):
        """
        on the first pass, store any (symbol) in the symbol table
        key = symbol
        value = line number

        Args:
            command (_type_): .asm command
            linenum (_type_): line number

        Returns:
            None/ str: return None if symbol else return back the command
        """
        sym = re.findall(r'\(.+\)',command)
        # L-Comand
        if sym != []:
            # found symbol
            _sym = sym[0][1:-1]
            if _sym not in MachineCode.symbols:
                MachineCode.symbols[_sym] = linenum # store current line location
            return None
        else:
            return command

    def convert_to_code(self, command):
        """
        convert parsed .asm file into 16-bit A-instruction or C-instruction

        A-command : '0' + 15-bit binary address
        C-command : 16-bit 111 + comp(6-bit) + dest(3-bit) + jump(3-bit)

        Returns:
        hcode(str): 16-bit binary code instruction
        """
        if command[0] == '@':
            # A-instruction
            address=0
            if command[1:] in MachineCode.symbols:
                # already in sym table
                address=bin(MachineCode.symbols[command[1:]])[2:].zfill(15) # parse number to binary and pad 0 to create 15-bit
            elif command[1:].isdigit():
                # @number
                address=bin(int(command[1:]))[2:].zfill(15)
            else:
                # variable
                MachineCode.symbols[command[1:]] = MachineCode.var
                address=bin(MachineCode.var)[2:].zfill(15)
                MachineCode.var += 1
            hcode = '0' + address + '\n'
        else:
            # C-instruction
            de = re.findall(r'.+=',command) # match pattern '...=', return x=
            if de != []:
                d = MachineCode.dest[str(de[0])] # d=destination code from dest hash.
            else:
                d = MachineCode.dest['']

            ju = re.findall(r';.+',command) # match pattern ';...'
            if ju != []:
                j = MachineCode.jump[str(ju[0])]
            else:
                j=MachineCode.jump['']

            comp_cmd = re.sub(r'.+=|;.+','',command) # extract the comp. string after = | string before ;
            c=MachineCode.comp[comp_cmd]
            hcode = '111' + c + d + j + '\n'
        return hcode

if __name__ == '__main__':
    pass
