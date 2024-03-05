# rewrite for vm code, discard xml
from SymbolTable import SymbolTable

class CompilationEngine:
    """_summary_
    token_file : token file path
    """

    VM_KIND = {
    'ARG': 'ARG',
    'STATIC': 'STATIC',
    'VAR': 'LOCAL',
    'FIELD': 'THIS'
    }

    UNARY_OPT = {
    '-': 'NEG',
    '~': 'NOT'
    }

    OPERATIONS = {
    '+': 'ADD',
    '-': 'SUB',
    '=': 'EQ',
    '>': 'GT',
    '<': 'LT',
    '&': 'AND',
    '|': 'OR'
    }

    def __init__(self, tokenizer, vm_writer):
        self.tokenizer = tokenizer
        self.vm_writer = vm_writer
        self.symbol_table = SymbolTable()

        self.while_index = -1
        self.if_index    = -1

    def compile_class(self):
        # Logic to compile a complete class

        self.tokenizer.advance()                            # skip 'class'
        self.class_name = self.tokenizer.get_curr_token()   # className
        self.tokenizer.advance()                            # skip className
        self.tokenizer.advance()                            # skip '{'

        while self.tokenizer.keyword() in ('static', 'field'):
            self.compile_class_var_dec()

        print("class table", self.symbol_table.class_scope)

        while self.tokenizer.keyword() in ('constructor', 'function', 'method'):
            self.compile_subroutine()

        # last token is '}' closing class
        if self.tokenizer.get_curr_token() == '}':
            self.vm_writer.close()
        else :
            raise ValueError(f"Missing closing class tag. Curr is {self.tokenizer.curr_token}")

    def compile_class_var_dec(self):
        # ('static' | 'field' ) type varName (',' varName)* ';'

        kind = self.tokenizer.get_curr_token()                # ('static' | 'field' )
        self.tokenizer.advance()
        type = self.tokenizer.get_curr_token()                    # type
        self.tokenizer.advance()
        name = self.tokenizer.get_curr_token()                    # varName
        self.tokenizer.advance()


        self.symbol_table.define(name, type, kind.upper())

        while self.tokenizer.get_curr_token() == ',':
            self.tokenizer.advance()                                # skip ','
            name = self.tokenizer.get_curr_token()                  # varName
            self.tokenizer.advance()
            self.symbol_table.define(name, type, kind.upper())

        self.tokenizer.advance()                 # Skip ';'
        print(self.tokenizer.curr_token)

    def compile_subroutine(self):
        # Logic to compile methods, functions, or constructors
        # subroutineDec: ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subroutineBody
        # subroutineBody: '{' varDec* statements '}'

        print("--- begin subroutine ---")

        print(self.tokenizer.curr_token)

        # setup
        self.symbol_table.startSubroutine()
        subroutine_kind = self.tokenizer.get_curr_token()       # ('constructor' | 'function' | 'method') if 'constructor', call Memory.alloc
        self.tokenizer.advance()

        if subroutine_kind == 'method':
            self.symbol_table.define('this', self.class_name, 'ARG')

        type = self.tokenizer.get_curr_token()                  # ('void' | type)
        self.tokenizer.advance()

        subroutine_name = self.tokenizer.get_curr_token()       # subroutineName
        self.tokenizer.advance()                                # skip subroutineName

        self.compile_parameter_list(type)                       # ( parameterList )

        # ----------------------
        # -- start subroutineBody
        # - declare variables
        self.tokenizer.advance()                    # skip '{'

        while self.tokenizer.curr_token == 'var':   # varDec* i.e. var int a; \n var char b;
            self.compile_var_dec()
        # ----

        # vm write
        num_locals = self.symbol_table.varCount('VAR')

        print("\n\n", self.symbol_table.subroutine_scope)
        self.vm_writer.writeFunction(f'{self.class_name}.{subroutine_name}', num_locals)

        if subroutine_kind == 'constructor':
            self.vm_writer.writePush("CONST", self.symbol_table.varCount('FIELD'))
            self.vm_writer.writeCall("Memory.alloc", 1)
            self.vm_writer.writePop("POINTER", 0)
        elif subroutine_kind == 'method':
            self.vm_writer.writePush("ARG", 0)          # push and pop 'this' reference to class
            self.vm_writer.writePop("POINTER", 0)

        self.compile_statements()                   # statements

        print(">>>", self.tokenizer.curr_token)

        self.tokenizer.advance()                    # skip '}' closing subroutine

        print("--- end subroutine --- \n\n\n")

        # -- end subroutineBody

    def compile_parameter_list(self, type):
        """
        Logic to compile a parameter list
        i.e. ((type arg0) , type arg1, type arg2, type arg3 )
        parameterList only exists as subroutine arguments

        subroutine : ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subroutineBody
        return : nArg
        """
        nArg = 0
        self.tokenizer.advance()                # skip '('

        if self.tokenizer.get_curr_token() != ')':
            type = self.tokenizer.get_curr_token()      # type
            self.tokenizer.advance()
            name = self.tokenizer.get_curr_token()      # arg0
            self.tokenizer.advance()
            self.symbol_table.define(name, type, 'ARG')
            nArg += 1

            while self.tokenizer.get_curr_token() != ')':
                self.tokenizer.advance()                    # skip ','
                type = self.tokenizer.get_curr_token()      # type
                self.tokenizer.advance()
                name = self.tokenizer.get_curr_token()      # arg1 ...
                self.tokenizer.advance()
                self.symbol_table.define(name, type, 'ARG')
                nArg += 1

        self.tokenizer.advance()            # skip ')'

        return nArg

    def compile_var_dec(self):
        # 'var' type varName (',' varName)* ';'
        kind = self.tokenizer.get_curr_token()                      # var
        self.tokenizer.advance()
        type = self.tokenizer.get_curr_token()                      # type
        self.tokenizer.advance()
        name = self.tokenizer.get_curr_token()                      # varName
        self.tokenizer.advance()

        self.symbol_table.define(name, type, kind.upper())

        while self.tokenizer.get_curr_token() == ',':
            self.tokenizer.advance()                                # skip ','
            name = self.tokenizer.get_curr_token()                  # varName
            self.tokenizer.advance()
            self.symbol_table.define(name, type, kind.upper())

        self.tokenizer.advance()  # Skip ';' at the end of the declaration
        print(self.symbol_table.subroutine_scope)
        print(self.symbol_table.class_scope)


    def compile_statements(self):
        # Logic to compile statements
        # letStatement | ifStatement | whileStatement | doStatement | returnStatement

        while self.tokenizer.get_curr_token() in ('let', 'if', 'while', 'do', 'return'):
            if self.tokenizer.get_curr_token() == 'let':
                self.compile_let()
            elif self.tokenizer.get_curr_token() == 'if':
                self.compile_if()
            elif self.tokenizer.get_curr_token() == 'while':
                self.compile_while()
            elif self.tokenizer.get_curr_token() == 'do':
                self.compile_do()
            elif self.tokenizer.get_curr_token() == 'return':
                self.compile_return()

    def compile_do(self):
        """
        # Logic to compile do statements
        # 'do' subroutineCall ';'
        # subroutineCall: subroutineName '(' expressionList ')' | ( className | varName) '.' subroutineName '(' expressionList ')'
        i.e. do Screen.drawRectangle(x, y, x+size, y+size);

        push arguments*
        call Foo.bar nArgs
        """
        # do
        self.tokenizer.advance()                # skip 'do'

        # subroutineCall
        self.compile_subroutine_call()
        self.vm_writer.writePop("TEMP",0)

        if self.tokenizer.get_curr_token() == ';':
            self.tokenizer.advance()          # ';'
        else:
            raise ValueError(f"Missing closing ; compile_do. Curr is {self.tokenizer.curr_token}")

    def compile_subroutine_call(self):
        print("--compile subroutinecall--")
        nArgs = 0       # count no. args needed
        identifier = self.tokenizer.get_curr_token()    # subroutineName or ( className | varName)
        self.tokenizer.advance()

        if self.tokenizer.get_curr_token() == '.':      # identifier is ( instance | class )
            self.tokenizer.advance()                    # skip .
            print("expecting print ", self.tokenizer.curr_token)
            if self.symbol_table.typeOf(identifier) is not None:
                # is instance, already defined in symbol table
                instance_kind = self.symbol_table.kindOf(identifier)
                instance_index = self.symbol_table.indexOf(identifier)

                self.vm_writer.writePush(self.VM_KIND[instance_kind], instance_index)  # push instance object ('this') as first arguemnt

                func_name = '{}.{}'.format(self.symbol_table.typeOf(identifier), self.tokenizer.get_curr_token())
                nArgs += 1
                print("TODO handle instance")
            else:
                # is class (not defined in Sym table)
                func_name = f'{identifier}.{self.tokenizer.get_curr_token()}'       # ( className | varName) '.' subroutineName
            self.tokenizer.advance()                                                # skip subroutineName
        else:
            # a method in this class
            func_name = f'{self.class_name}.{identifier}'
            nArgs = 1
            self.vm_writer.writePush('POINTER', 0)      # call method in same class, push this as first argument.

        # push arguments (if any)
        nArgs += self.compile_expression_list()                                     # ( expressionList )

        print("-- end expression list -- ", self.tokenizer.curr_token)

        self.vm_writer.writeCall(func_name, nArgs)                                 # call Screen.drawRectangle 4


    def compile_let(self):
        # 'let' varName ('[' expression ']')? '=' expression ';'
        # let always inside subroutine
        """_summary_

        Array:
            // arr [exp1] = exp2
            push arr
            (vm code for exp1)
            add
            (vm code for exp2)
            pop temp 0
            pop pointer 1
            push temp 0
            pop that 0
        """
        self.tokenizer.advance()                        # skip 'let'

        var_name = self.tokenizer.get_curr_token()          # varName
        var_kind = self.VM_KIND[self.symbol_table.kindOf(var_name)]
        var_index = self.symbol_table.indexOf(var_name)
        self.tokenizer.advance()                        # skip varName

        # check variable in symbol table
        print("subroutine table", self.symbol_table.subroutine_scope)
        print("class table", self.symbol_table.class_scope)

        if '[' in self.tokenizer.get_curr_token():
            # array assignment ('[' expression ']')?
            self.tokenizer.advance()                    # '['
            self.compile_expression()                   # expression 1
            self.tokenizer.advance()                    # ']'

            self.vm_writer.writePush(var_kind, var_index)
            self.vm_writer.writeArithmetic("ADD")

            self.tokenizer.advance()                        # '=' ops
            self.compile_expression()                       # expression 2

            self.vm_writer.writePop("TEMP", 0)  # assign value
            self.vm_writer.writePop("POINTER", 1)  # assign value
            self.vm_writer.writePush("TEMP", 0)  # assign value
            self.vm_writer.writePop("THAT", 0)  # assign value

        else :     # normal assignment
            self.tokenizer.advance()                        # '=' ops
            self.compile_expression()                       # expression

            self.vm_writer.writePop(var_kind, var_index)  # assign value

        if self.tokenizer.get_curr_token() == ';':
            self.tokenizer.advance()                       #  skip ';'
        else:
            raise ValueError("Missing closing ; in compile_let. Curr: ", self.tokenizer.curr_token)

    def compile_while(self):
        """
        'while' '(' expression ')' '{' statements '}'

        label L1
            compiled (expression)
            not
            if-goto L2                  // if true go to L2
            compiled (statements)       // { statement }
            goto L1                     // go always
        label L2                        // end

        """
        self.tokenizer.advance()    #   skip 'while'

        self.while_index += 1
        label1 = f'WHILE{self.while_index}'
        label2 = f'WHILE_END{self.while_index}'
        self.vm_writer.writeLabel(label1)

        self.tokenizer.advance()    # skip '('

        self.compile_expression()   # expression
        self.tokenizer.advance()    # ')'

        self.vm_writer.writeArithmetic("NOT")
        self.vm_writer.writeIf(label2)

        self.tokenizer.advance()    # '{'
        self.compile_statements()   # statements
        self.tokenizer.advance()     # '}' closing while

        self.vm_writer.writeGoto(label1)

        self.vm_writer.writeLabel(label2)

    def compile_return(self):
        #
        """
        'return' expression? ';'
        i.e. return; | return result; | return a*b; |
        """
        self.tokenizer.advance()    # skip return

        if self.tokenizer.get_curr_token() == ';':      # return void
            self.vm_writer.writePush("CONST", 0)
        else :
            self.compile_expression()

        self.tokenizer.advance()      # skip ;
        self.vm_writer.writeReturn()



    def compile_if(self):
        # 'if' '(' expression ')' '{' statements '}' ( 'else' '{' statements '}' )?
        """
        compiled (expression)
            not
            if-goto L1
            compiled (statements1)
            goto L2
        label L1
            compiled (statements2)      // else statement
        label L2                        // end
        """

        self.if_index += 1
        label1 = f'IF_FALSE{self.if_index}'
        label2 = f'IF_END{self.if_index}'

        self.tokenizer.advance()        # skip 'if'
        self.tokenizer.advance()        # skip '('

        self.compile_expression()       # expression
        self.tokenizer.advance()        # skip ')'

        self.vm_writer.writeArithmetic("NOT")       ## not
        self.vm_writer.writeIf(label1)              ## if-goto L1

        self.tokenizer.advance()        # skip '{'
        self.compile_statements()       # statements 1
        self.tokenizer.advance()        # skip '}'

        self.vm_writer.writeGoto(label2)            ## goto L2

        self.vm_writer.writeLabel(label1)           ## L1

        if self.tokenizer.get_curr_token() == 'else':
            self.tokenizer.advance()     # skip 'else'
            self.tokenizer.advance()     # skip '{'

            self.compile_statements()    # 'statements' 2
            self.tokenizer.advance()     # skip '}'

        self.vm_writer.writeLabel(label2)           ## L2

    def compile_expression(self):
        # term (op term)*
        # i.e. a + b
        # if expression -> compile normally
        # if ( expression ) -> term will handle '(' and ')'
        self.compile_term()             # a
        print("\n\n\n----- op: ", self.tokenizer.get_curr_token())

        while self.tokenizer.get_curr_token() in ('+', '-', '*', '/', '&', '|' , '<', '>', '='):
            op = self.tokenizer.get_curr_token()                        # op
            self.tokenizer.advance()
            self.compile_term()                                         # b

            # write ops
            if op in self.OPERATIONS:
                self.vm_writer.writeArithmetic(self.OPERATIONS[op])     # op
            elif op == '*':
                self.vm_writer.writeCall('Math.multiply', 2)
            elif op == '/':
                self.vm_writer.writeCall('Math.divide', 2)

            # if self.tokenizer.get_curr_token() == ')':
            #     print("exepection ')'", self.tokenizer.curr_token)
            #     self.tokenizer.advance()
        print("--- end expression -- curr :", self.tokenizer.get_curr_token())



    def compile_term(self):

        # integerConstant | stringConstant | keywordConstant | varName |
        # varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOp term

        token = self.tokenizer.get_curr_token()
        tokenType = self.tokenizer.token_type
        print(f"-- compile term -- name : {token} type: {tokenType}--")

        if tokenType == 'INT_CONSTANT':
            # print("expecting int ", self.tokenizer.get_curr_token())
            self.vm_writer.writePush('CONST', token)
            self.tokenizer.advance()
        elif tokenType == 'STRING_CONSTANT':
            # TODO
            #
            self.compileStringConstant(token)
            self.tokenizer.advance()
        elif tokenType == 'KEYWORD':
            # KeywordConstant : this | true | false | null
            if token == 'this':
                self.vm_writer.writePush('POINTER', 0)
            elif token in ('true', 'false', 'null'):
                self.vm_writer.writePush('CONST', 0)
                if token == 'true':
                    self.vm_writer.writeArithmetic('NOT')
            self.tokenizer.advance()
        elif tokenType == 'SYMBOL':
            if token in {'-', '~'}:                     # unaryOp
                self.tokenizer.advance()                # skip op
                self.compile_term()                     # term
                self.vm_writer.writeArithmetic(self.UNARY_OPT[token])
            elif token == '(':
                self.tokenizer.advance()                # (
                self.compile_expression()
                print("~~~~closing ) in term", self.tokenizer.curr_token)
                self.tokenizer.advance()                # )
        elif tokenType == 'IDENTIFIER':
            # handle variable , array, subroutineCall
            # varName | varName [expression] | subroutineCall
            # i.e. foo | foo[..] | SomeClass.foo(expressionList) | foo(expressionList)

            peek = self.peek_token()

            if peek == '[':
                # compile term varName '[' expression ']' "

                arr_var = self.tokenizer.get_curr_token()   # varName
                arr_kind = self.VM_KIND[self.symbol_table.kindOf(arr_var)]
                arr_index = self.symbol_table.indexOf(arr_var)
                self.tokenizer.advance()                    # skip varName

                self.tokenizer.advance()                    # '['
                self.compile_expression()                    # push expression
                self.tokenizer.advance()                    # ']'

                self.vm_writer.writePush(arr_kind, arr_index)

                self.vm_writer.writeArithmetic('ADD')
                self.vm_writer.writePop('POINTER', 1)
                self.vm_writer.writePush('THAT', 0)

            elif peek in ('(', '.'):
                # subroutine call
                self.compile_subroutine_call()
            else:
                # a variable / symbol
                kind = self.symbol_table.kindOf(token)
                if kind is None:
                    # new symbol ?
                    pass
                else :
                    # push symbol
                    self.vm_writer.writePush(self.VM_KIND[kind], self.symbol_table.indexOf(token))
                    print(f"push {self.tokenizer.curr_token}")
                self.tokenizer.advance()

        else:
            # Handle unexpected token type
            raise ValueError("Unexpected token type")


    def compile_expression_list(self):
        # Logic to compile expression lists (used in subroutine calls)
        # (expression (',' expression)* )? i.e. (x, y, Ax, Ay);
        print("--compile expression list --")
        nArgs = 0
        if self.tokenizer.get_curr_token() == '(':
            self.tokenizer.advance()                            # skip '('

        if self.tokenizer.get_curr_token() != ')':
            self.compile_expression()                       # first expression
            nArgs = 1

            while self.tokenizer.get_curr_token() != ')':
                self.tokenizer.advance()                    # ','
                self.compile_expression()                   # expression

                nArgs += 1
                print("\t>>>getting next args cur: " ,self.tokenizer.curr_token)

        if self.tokenizer.get_curr_token() == ')':
            self.tokenizer.advance()
        else:
            raise ValueError(f"Missing Closing ) compile_expression_list. Curr is {self.tokenizer.curr_token}")

        return nArgs

    # ------------------ END COMPILER API -----------------------


    # ------------------ COMPILER API HELPER -----------------------

    def compileStringConstant(self, string):
        # TODO
        self.vm_writer.writePush('CONST', len(string))
        self.vm_writer.writeCall('String.new', 1)

        for char in string:
            self.vm_writer.writePush('CONST', ord(char))
            self.vm_writer.writeCall('String.appendChar', 2)

    # def compileKeywordConstant(self):
    #     self.output_stream.write(f"{self.current_indent()}<KeywordConstant> {self.tokenizer.get_curr_token()} </KeywordConstant>\n")
    #     self.is_written = True
    #     return

    # ------------------ COMPILER UTILS -----------------------

    def write_next_token(self):         # delete
        # if curr is written, load next
        self.load_next_token_as_not_written()
        # write xml
        self.output_stream.write(f"{self.current_indent()}<{self.tokenizer.token_type.lower()}> {self.tokenizer.get_curr_token()} </{self.tokenizer.token_type.lower()}>\n")
        self.is_written = True
        return

    def load_next_token_as_not_written(self): # delete
        # if curr already written, load next token, mark newly loaded as not written
        if self.is_written:
            self.tokenizer.advance()
            self.is_written = False

    def peek_token(self):
        """ return the preview of next token """
        peek = self.tokenizer.jack.popleft()
        self.tokenizer.jack.appendleft(peek)    # push token back to the front of list
        return peek[0]

    def current_indent(self): # delete
        return '  ' * self.indent_count
