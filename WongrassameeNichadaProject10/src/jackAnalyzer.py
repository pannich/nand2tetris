'''
jackAnalyzer

Nichada Wongrassamee
'''
from program0 import parseempty
import sys
from collections import deque

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

class JackTokenizer:
    """set curr_token and token_type

    Returns:
        _type_: _description_
    """
    symbol_set = set(['{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<','>','=','~',])
    keyword_set = set([
            'class',
            'constructor',
            'function',
            'method',
            'field',
            'static',
            'var',
            'int',
            'char',
            'boolean',
            'void',
            'true',
            'false',
            'null',
            'this',
            'let',
            'do',
            'if',
            'else',
            'while',
            'return']
    )
    #----------------------
    #--- API
    def __init__(self, jack_file):
        """Args:
            jack_file : <filepath>.out
        """
        self.jack_file = jack_file
        self.jack = self.load_jack(self.jack_file)
        self.curr_token = None
        self.token_type = None

        self.filename_no_ext = self.jack_file.split("/")[-1].replace(".out","")

        out_file = jack_file.replace(".out", "T.xml") # Token filepath
        self.out_file = open(out_file, 'w')
        self.out_file.write(f"<tokens>\n")


    def has_more_tokens(self):
        # `if has_more_tokens`` return False if self.jack is an empty queue
        if not self.jack:
            self.out_file.write(f"</tokens>\n")         # close file
        return self.jack

    def advance(self):
        next_token = self.jack.popleft()

        # Symbol
        if next_token[0] in self.symbol_set:
            self.token_type = 'SYMBOL'
            self.curr_token = next_token[0]
            if self.curr_token == '<':
                self.curr_token = '&lt;'
            elif self.curr_token == '>':
                self.curr_token = '&gt;'
            elif self.curr_token == '&':
                self.curr_token = '&amp;'

            if next_token[1:]:
                self.jack.appendleft(next_token[1:])
            self.out_file.write(f"<symbol> {self.curr_token} </symbol>\n")
            return

        # Integer Constant
        if next_token[0].isdigit():
            self.token_type = 'INT_CONSTANT'
            for i, letter in enumerate(next_token):
                if not next_token[i].isdigit():
                    self.curr_token = next_token[:i]
                    self.out_file.write(f"<integerConstant> {self.curr_token} </integerConstant>\n")
                    if next_token[i:]: # if has more to parse, push it back to self.jack
                        self.jack.appendleft(next_token[i:])
                        return

        # String Constant
        if next_token[0] == '"':
            self.token_type = 'STRING_CONSTANT'
            # parse string wo double quote i.e. "THE AVERAGE IS: ");
            curr_string = next_token[1:]
            str_ = ''

            while curr_string:
                for i, letter in enumerate(curr_string):
                    if letter == '"':
                        str_ += curr_string[:i].strip()
                        if curr_string[i+1:]: # if has more to parse
                            self.jack.appendleft(curr_string[i+1:])     # ';'
                            self.curr_token = str_                      # set curr_token before returning
                            self.out_file.write(f"<stringConstant> {self.curr_token} </stringConstant>\n")
                            return

                # if not found closing " yet
                str_ += curr_string
                if self.has_more_tokens():
                    str_ += ' '
                    curr_string = self.jack.popleft()


        # Else, Identifier or Keyword
        #   Identifier is a variable alone
        #   Keyword has symbol trailing
        self.curr_token = next_token    # set whole token as curr
        for i, letter in enumerate(next_token):
            if letter in self.symbol_set:
                self.curr_token = next_token[:i]    # update curr_token if found symbol
                self.jack.appendleft(next_token[i:])
                break
        if self.curr_token in self.keyword_set:
            self.token_type = 'KEYWORD'
            self.out_file.write(f"<keyword> {self.curr_token} </keyword>\n")
        elif self.curr_token:   # if not empty  #(TODO parse empty since the load_jack part)
            self.token_type = 'IDENTIFIER'
            self.out_file.write(f"<identifier> {self.curr_token} </identifier>\n")
        return

    def keyword(self):
        return self.curr_token if self.curr_token in self.keyword_set else None

    def symbol(self):
        return self.curr_token

    def identifier(self):
        return self.curr_token

    def int_val(self):
        return int(self.curr_token)

    def string_val(self):
        return self.curr_token

    #--- end API
    #----------------------

    def load_jack(self, jack_file):
        tokens = []
        with open(jack_file, "r") as fd:
            for line in fd:
                tokens.extend(line.split())
        return deque(tokens)

    # def write_Txml(self):
    #     self.out_file.write(f"<tokens>\n")

    #     while self.has_more_tokens():
    #         self.advance()
    #     self.out_file.write(f"</tokens>\n")
    #     self.out_file.close()

class CompilationEngine:
    """_summary_
    token_file : token file path
    """
    def __init__(self, tokenizer, output_stream):
        self.tokenizer = tokenizer # TODO change to parsing the token file

        self.output_stream = open(output_stream, 'w')
        self.indent_count = 0
        self.is_written = False

    def compile_class(self):
        # Logic to compile a complete class
        self.output_stream.write(f"{self.current_indent()}<class>\n")
        self.indent_count += 1

        self.write_next_token() # 'class'
        self.write_next_token() # className
        self.write_next_token() # '{'

        self.load_next_token_as_not_written()
        # print(self.tokenizer.curr_token, self.is_written)

        while self.tokenizer.keyword() in ('static', 'field'):
            self.compile_class_var_dec()
            self.load_next_token_as_not_written()

        while self.tokenizer.keyword() in ('constructor', 'function', 'method'):
            self.compile_subroutine()
            self.load_next_token_as_not_written()

        self.write_next_token() # '}'
        print("--end compile class--")

        self.indent_count -= 1
        self.output_stream.write(f"{self.current_indent()}</class>\n")

    def compile_class_var_dec(self):
        # ('static' | 'field' ) type varName (',' varName)* ';'
        self.output_stream.write(f"{self.current_indent()}<classVarDec>\n")
        self.indent_count += 1

        self.write_next_token()                   # ('static' | 'field' )
        self.write_next_token()                   # type
        self.write_next_token()                   # varName
        self.load_next_token_as_not_written()

        # Handle varName and possible comma-separated list of varNames
        while self.tokenizer.curr_token == ',':
            self.write_next_token()                # ','
            self.write_next_token()                # varName
            self.load_next_token_as_not_written()

        self.write_next_token()                     # ';'
        self.indent_count -= 1
        self.output_stream.write(f"{self.current_indent()}</classVarDec>\n")

    def compile_subroutine(self):
        # Logic to compile methods, functions, or constructors
        # subroutineDec: ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subroutineBody
        # subroutineBody: '{' varDec* statements '}'
        self.output_stream.write(f"{self.current_indent()}<subroutineDec>\n")
        self.indent_count += 1

        self.write_next_token()       # ('constructor' | 'function' | 'method')
        self.write_next_token()       # ('void' | type)
        self.write_next_token()       # subroutineName
        self.write_next_token()       # '('
        self.load_next_token_as_not_written()       # advance

        self.compile_parameter_list()               # parameterList
        self.load_next_token_as_not_written()       # advance

        # -- start subroutineBody
        self.write_next_token()                     # ')'
        self.output_stream.write(f"{self.current_indent()}<subroutineBody>\n")
        self.indent_count += 1
        self.write_next_token()                     # '{'

        self.load_next_token_as_not_written()       # varDec*
        while self.tokenizer.curr_token == 'var':
            self.compile_var_dec()                    # varDec*
            self.load_next_token_as_not_written()

        self.compile_statements()                   # statements

        self.write_next_token()                     # '}'

        self.indent_count -= 1
        self.output_stream.write(f"{self.current_indent()}</subroutineBody>\n")
        # -- end subroutineBody

        self.indent_count -= 1
        self.output_stream.write(f"{self.current_indent()}</subroutineDec>\n")


    def compile_parameter_list(self):
        # Logic to compile a parameter list
        print("compile parameter list")
        self.output_stream.write(f"{self.current_indent()}<parameterList>\n")
        self.indent_count += 1

        ### dummy
        while self.tokenizer.curr_token != ')':
            self.write_next_token()       # parameterList things to skip
            self.load_next_token_as_not_written()
            print("next", self.tokenizer.curr_token)

        print("done parameter list")

        self.indent_count -= 1
        self.output_stream.write(f"{self.current_indent()}</parameterList>\n")

    def compile_var_dec(self):
        # 'var' type varName (',' varName)* ';'
        self.output_stream.write(f"{self.current_indent()}<varDec>\n")
        self.indent_count += 1

        self.write_next_token()                 # ('static' | 'field' )
        self.write_next_token()                 # type
        self.write_next_token()                 # varName
        self.load_next_token_as_not_written()

        while self.tokenizer.curr_token == ',':
            self.write_next_token()                 # ','
            self.write_next_token()                 # varName

        self.write_next_token()                     # ';'

        self.indent_count -= 1
        self.output_stream.write(f"{self.current_indent()}</varDec>\n")

    def compile_statements(self):
        # Logic to compile statements
        # letStatement | ifStatement | whileStatement | doStatement | returnStatement
        self.output_stream.write(f"{self.current_indent()}<statements>\n")
        self.indent_count += 1

        print("--compile statements--", self.tokenizer.curr_token)

        while self.tokenizer.curr_token in ('let', 'if', 'while', 'do', 'return'):
            if 'let' in self.tokenizer.curr_token:
                self.compile_let()
            elif 'if' in self.tokenizer.curr_token:
                self.compile_if()
            elif 'while' in self.tokenizer.curr_token:
                self.compile_while()
            elif 'do' in self.tokenizer.curr_token:
                self.compile_do()
            elif 'return' in self.tokenizer.curr_token:
                self.compile_return()
            self.load_next_token_as_not_written()

        self.indent_count -= 1
        self.output_stream.write(f"{self.current_indent()}</statements>\n")

    def compile_do(self):
        # Logic to compile do statements
        # 'do' subroutineCall ';'
        # subroutineCall: subroutineName '(' expressionList ')' | ( className | varName) '.' subroutineName '(' expressionList ')'
        self.output_stream.write(f"{self.current_indent()}<doStatement>\n")
        self.indent_count += 1

        # do
        self.write_next_token()   # 'do'

        # subroutineCall
        self.write_next_token()   # subroutineName or ( className | varName)
        self.load_next_token_as_not_written()

        if self.tokenizer.curr_token == '.':
            self.write_next_token()   # .
            self.write_next_token()   # subroutineName

        self.write_next_token()          # (
        self.load_next_token_as_not_written()

        self.compile_expression_list()   # expressionList
        self.write_next_token()          # ')'
        self.write_next_token()          # ';'

        print("finish compile do", self.tokenizer.curr_token)

        self.indent_count -= 1
        self.output_stream.write(f"{self.current_indent()}</doStatement>\n")

    def compile_let(self):
        # 'let' varName ('[' expression ']')? '=' expression ';'
        # Logic to compile let statements
        self.output_stream.write(f"{self.current_indent()}<letStatement>\n")
        self.indent_count += 1

        self.write_next_token()                         # 'let'
        self.write_next_token()                         # varName

        self.load_next_token_as_not_written()           # mark newly loaded as not written

        if '[' in self.tokenizer.curr_token:            # ('[' expression ']')?
            self.write_next_token()       # '['
            self.compile_expression()                   # expression
            self.write_next_token()                     # ']'

        self.write_next_token()                         # '=' ops
        self.compile_expression()                       # expression

        # Writing the semicolon and closing tag
        self.write_next_token()                         #  ';'
        self.indent_count -= 1
        self.output_stream.write(f"{self.current_indent()}</letStatement>\n")

    def compile_while(self):
        # 'while' '(' expression ')' '{' statements '}'
        print("TODO compile while")
        self.output_stream.write(f"{self.current_indent()}<whileStatement>\n")
        self.indent_count += 1

        self.write_next_token()     # while
        self.write_next_token()     # '('
        self.load_next_token_as_not_written()

        self.compile_expression()   # expression
        self.write_next_token()     # ')'
        self.write_next_token()     # '{'
        self.load_next_token_as_not_written()

        self.compile_statements()   # statements
        self.write_next_token()     # '}'

        self.indent_count -= 1
        self.output_stream.write(f"{self.current_indent()}</whileStatement>\n")


        pass

    def compile_return(self):
        # Logic to compile return statements
        # 'return' expression? ';'
        self.output_stream.write(f"{self.current_indent()}<returnStatement>\n")
        self.indent_count += 1

        self.write_next_token()                         # return
        self.load_next_token_as_not_written()

        if self.tokenizer.curr_token != ';':            # expression?
            self.compile_expression()

        self.write_next_token()                         # ;
        print("---finish return---")

        self.indent_count -= 1
        self.output_stream.write(f"{self.current_indent()}</returnStatement>\n")

    def compile_if(self):
        # 'if' '(' expression ')' '{' statements '}' ( 'else' '{' statements '}' )?
        self.output_stream.write(f"{self.current_indent()}<ifStatement>\n")
        self.indent_count += 1

        self.write_next_token()     # 'if'
        self.write_next_token()     # '('
        self.load_next_token_as_not_written()

        self.compile_expression()   # expression
        self.write_next_token()     # ')'
        self.write_next_token()     # '{'
        self.load_next_token_as_not_written()

        self.compile_statements()   # statements
        self.write_next_token()     # '}'
        self.load_next_token_as_not_written()

        if self.tokenizer.curr_token == 'else':
            self.write_next_token()     # 'else'
            self.write_next_token()     # '{'
            self.load_next_token_as_not_written()

            self.compile_statements()   # 'statements'
            self.write_next_token()     # '}'

        self.indent_count -= 1
        self.output_stream.write(f"{self.current_indent()}</ifStatement>\n")

    def compile_expression(self):
        # term (op term)*
        self.output_stream.write(f"{self.current_indent()}<expression>\n")
        self.indent_count += 1

        self.load_next_token_as_not_written()
        self.compile_term()
        self.load_next_token_as_not_written()

        while self.tokenizer.curr_token in ('+', '-', '*', '/', '&amp;', '|' , '&lt;', '&gt;', '='):
            self.write_next_token()                     # op
            self.compile_term()                         # term
            self.load_next_token_as_not_written()

        # Writing the semicolon and closing tag
        self.indent_count -= 1
        self.output_stream.write(f"{self.current_indent()}</expression>\n")

    def compile_term(self):
        # Logic to compile terms
        # integerConstant | stringConstant | keywordConstant | varName |
        # varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOp term
        self.output_stream.write(f"{self.current_indent()}<term>\n")
        self.indent_count += 1

        self.load_next_token_as_not_written()

        tokenType = self.tokenizer.token_type

        print("---compile TERM---")


        if tokenType == 'INT_CONSTANT':
            self.compileIntegerConstant()
        elif tokenType == 'STRING_CONSTANT':
            self.compileStringConstant()
        elif tokenType == 'KEYWORD':
            self.write_next_token()
        elif tokenType == 'IDENTIFIER':
            # handle subroutinecall identifier '[' or ('(', '.'), else identifier

            peek = self.peek_token()
            print(self.tokenizer.curr_token, tokenType, "peek", peek)

            if peek == '[':
                # TODO compile array?
                print("compile term varName '[' expression ']' ")
                self.write_next_token()                 # varName
                self.write_next_token()                 # '['
                self.load_next_token_as_not_written()
                self.compile_expression()
                self.write_next_token()                 # ']'

            elif peek in ('(', '.'):
                # subroutine call
                self.write_next_token()                 # subroutineName , classame | varName
                self.load_next_token_as_not_written()
                if self.tokenizer.curr_token == '.':
                    self.write_next_token()             # .
                    self.write_next_token()             # subroutineName

                self.write_next_token()                 # (
                self.load_next_token_as_not_written()

                self.compile_expression_list()          # expressionList
                self.write_next_token()                 # ')'
            else:
                self.write_next_token()                 # write identifier
        elif tokenType == 'SYMBOL':
            if self.tokenizer.symbol() in {'-', '~'}:   # unaryOp
                self.write_next_token()
                self.load_next_token_as_not_written
                self.compile_term()
            elif self.tokenizer.symbol() == '(':
                print("get here!")
                self.write_next_token()
                self.compile_expression()
                self.write_next_token()

        else:
            # Handle unexpected token type
            raise ValueError("Unexpected token type")

        print("end compile term")
        self.load_next_token_as_not_written()           # advance

        self.indent_count -= 1
        self.output_stream.write(f"{self.current_indent()}</term>\n")

    def compile_expression_list(self):
        # Logic to compile expression lists (used in subroutine calls)
        # (expression (',' expression)* )? i.e. (x, y, x, y);
        print("compile expressionList")
        self.output_stream.write(f"{self.current_indent()}<expressionList>\n")
        self.indent_count += 1

        if self.tokenizer.curr_token != ')':
            while self.tokenizer.curr_token != ')':
                if self.tokenizer.curr_token == ',':
                    self.write_next_token()               # ,
                else:
                    self.compile_expression()            # expression
                self.load_next_token_as_not_written()

        self.indent_count -= 1
        self.output_stream.write(f"{self.current_indent()}</expressionList>\n")

    # ------------------ END COMPILER API -----------------------


    # ------------------ COMPILER API HELPER -----------------------
    def compileIntegerConstant(self):
        self.output_stream.write(f"{self.current_indent()}<integerConstant> {self.tokenizer.curr_token} </integerConstant>\n")
        self.is_written = True
        return

    def compileStringConstant(self):
        self.output_stream.write(f"{self.current_indent()}<stringConstant> {self.tokenizer.curr_token} </stringConstant>\n")
        self.is_written = True
        return

    def compileKeywordConstant(self):
        self.output_stream.write(f"{self.current_indent()}<KeywordConstant> {self.tokenizer.curr_token} </KeywordConstant>\n")
        self.is_written = True
        return

    # ------------------ COMPILER UTILS -----------------------

    def write_next_token(self):
        # if curr is written, load next
        self.load_next_token_as_not_written()

        # debug
        print(f"// {self.current_indent()}<{self.tokenizer.token_type.lower()}> {self.tokenizer.curr_token} </{self.tokenizer.token_type.lower()}>\n")

        # write xml
        self.output_stream.write(f"{self.current_indent()}<{self.tokenizer.token_type.lower()}> {self.tokenizer.curr_token} </{self.tokenizer.token_type.lower()}>\n")
        self.is_written = True
        return

    def load_next_token_as_not_written(self):
        # if curr already written, load next token, mark newly loaded as not written
        if self.is_written:
            self.tokenizer.advance()
            self.is_written = False
            # print("loaded next :", self.tokenizer.curr_token, "status: ", self.is_written)

    def peek_token(self):
        peek = self.tokenizer.jack.popleft()
        self.tokenizer.jack.appendleft(peek)
        return peek[0]

    def current_indent(self):
        return '  ' * self.indent_count

def main():
    output_stream = sys.argv[1].replace(".jack", ".xml")  # not overwrite original

    remove_comment = RemoveComment(sys.argv[1])
    filepath_parsed_comment = remove_comment.parse_comment() # <filepath>.out

    # TODO change reload tokenizer
    tokenizer   = JackTokenizer(filepath_parsed_comment)
    compiler    = CompilationEngine(tokenizer, output_stream)

    while tokenizer.has_more_tokens():
        tokenizer.advance()
        if tokenizer.keyword() == 'class':
            compiler.compile_class()
    return

if __name__ == "__main__":
    main()


# TODO test tokenizer
