from parser import parseempty
import MachineCode
import sys
import os


def extract_filename(input_file_path):
    """
    check if input file is .asm file

    Return:
        None if file not valid
        filename if file has valid extension
    """
    try:
        filename = sys.argv[1][:-4]  # parse filename
        extension = sys.argv[1][-3:]
        if extension != "asm":
            raise ValueError("File is not a .asm input")
    except ValueError as e:
        print(f"Error: {e}")
        return None
    return filename


def pass1(filein, fileout):
    """
    parse <filein>.asm into <fileout>.out

    Args:
        filein (str.asm): input file
        fileout (str): <filepath>.out
    """
    # parse new line and comment into .hack file
    with open(f"{fileout}", "w") as fout:
        with open(f"{filein}", "r") as fd:
            comment = False  # comment status at the beginning of the file
            for line in fd:
                linenospace, comment = parseempty(line, comment)
                if linenospace and linenospace != "\n":
                    # write to output file
                    fout.write(linenospace)


def pass2(machinecode, in_file, out_file):
    """
    convert .asm file into hack file
    Args:
        machinecode (obj) : object class MachineCode()
        in_file (str): <filepath>1.out
        out_file (str): <filepath>2.out
    """
    with open(f"{out_file}", "w") as fout:
        with open(f"{in_file}", "r") as fd:
            linenum = 0
            for command in fd:
                line = machinecode.store_symbol(command, linenum)
                if line:  # if not a symbol
                    fout.write(line)
                    linenum += 1


def pass3(machinecode, in_file, out_file):
    """
    convert .asm file into hack file

    Args:
        machinecode (obj) : object class MachineCode()
        in_file (str): filepath.asm
        out_file (str): filepath.hack
    """
    with open(f"{out_file}", "w") as fout:
        with open(f"{in_file}", "r") as fd:
            for command in fd:
                hcode = machinecode.convert_to_code(
                    command[:-1]
                )  # parseing the command without the \n
                fout.write(hcode)


def main():
    input_file_path = sys.argv[1]

    filename = extract_filename(input_file_path)

    if filename is None:
        return

    # machinecode object
    machinecode = MachineCode.MachineCode()

    # first pass
    pass1(f"{filename}.asm", f"{filename}1.out")

    # second pass
    pass2(machinecode, f"{filename}1.out", f"{filename}2.out")

    # thrid pass
    pass3(machinecode, f"{filename}2.out", f"{filename}.hack")

    # clean up
    os.remove(f"{filename}1.out")
    os.remove(f"{filename}2.out")

if __name__ == "__main__":
    main()
