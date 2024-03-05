'''
JackTokenizer

Nichada Wongrassamee
'''

from collections import deque

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
            self.out_file.close()                       # new
        return self.jack

    def advance(self):
        next_token = self.jack.popleft()
        print(f"->{next_token}")

        # Symbol
        if next_token[0] in self.symbol_set:
            self.token_type = 'SYMBOL'
            self.curr_token = next_token[0]
            # if self.curr_token == '<':
            #     self.curr_token = '&lt;'
            # elif self.curr_token == '>':
            #     self.curr_token = '&gt;'
            # elif self.curr_token == '&':
            #     self.curr_token = '&amp;'

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
                        print("integer: " , self.curr_token, self.token_type)
                        return
            # if the whole next_token is digit
            self.curr_token = next_token
            self.out_file.write(f"<integerConstant> {self.curr_token} </integerConstant>\n")
            print("integer: " , self.curr_token, self.token_type)
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
        elif self.curr_token:   # if not empty  #(parse empty since the load_jack part)
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

    def get_curr_token(self):
        return self.curr_token

    #--- end API
    #----------------------

    def load_jack(self, jack_file):
        tokens = []
        with open(jack_file, "r") as fd:
            for line in fd:
                tokens.extend(line.split())
        return deque(tokens)

    def write_Txml(self):
        # for debugging
        self.out_file.write(f"<tokens>\n")

        while self.has_more_tokens():
            self.advance()
