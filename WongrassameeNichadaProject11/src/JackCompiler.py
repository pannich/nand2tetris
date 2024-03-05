'''
JackCompiler - Main

Nichada Wongrassamee
'''

from program0 import parseempty
import sys, os, glob
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine
from VMWriter import VMWriter

class RemoveComment:
    """
    parse <filein>.jack into <fileout>.out

    Args:
        filein (str.jack): input filepath
        fileout (str): <filepath>.out
    """
    def __init__(self, arg) -> None:
        self.arg = arg
        self.ext = ".jack"
        self.filename_no_ext = self.extract_filename()
        self.in_file = f'{self.filename_no_ext}.jack'
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
        print(self.out_file)
        return self.out_file

def jack_compile(jack_file):
    output_stream = jack_file.replace(".jack", ".vm")

    remove_comment = RemoveComment(jack_file)
    filepath_parsed_comment = remove_comment.parse_comment() # <filepath>.out

    tokenizer   = JackTokenizer(filepath_parsed_comment)
    # tokenizer.write_Txml()
    vm_writer   = VMWriter(output_stream)
    compiler    = CompilationEngine(tokenizer, vm_writer)

    while tokenizer.has_more_tokens():
        tokenizer.advance()
        if tokenizer.keyword() == 'class':
            compiler.compile_class()

    #clean up
    os.remove(jack_file.replace(".jack", ".out"))
    os.remove(jack_file.replace(".jack", "T.xml"))
    return

def main():
    file_path = sys.argv[1]
    file_path = file_path[:-1] if file_path[-1] == '/' else file_path   # ie. tests/ConvertToBin or tests/ConvertToBin/Main.jack

    file_dir, _ext = os.path.splitext(file_path)
    if _ext == '.jack':
        # a single file
        jack_files = [file_path]
    else:
        # a directory
        pattern = os.path.join(file_dir, '*.jack')        # ie. tests/ConvertToBin/*.vm
        jack_files = glob.glob(pattern) # a list

    print(jack_files)

    for jack in jack_files:
        jack_compile(jack)


if __name__ == "__main__":
    main()
