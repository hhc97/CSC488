#!/usr/bin/env python3

from ply import yacc
from calculatorLexer import calculatorLexer
from calculatorLexer import tokens

class calculatorParser:

    # Refer to calculatorLexer.py for the tokens which needs to be parsed.
    # Things to consider:
    # - order of operation
    # - ambiguity
    # - parser structure

    def p_expr(self, p):
        '''
        expr : NUMBER
        '''
        #^       ^
        #p[0]   p[1]

        p[0] = p[1]

    # Error handling rule
    def p_error(self, p):
        print("Syntax error in input!")

    # Build the parser
    def build(self, **kwargs):
        self.tokens = tokens
        self.lexer = calculatorLexer()
        self.lexer.build()
        self.parser = yacc.yacc(module=self, **kwargs)

    # Show the prompt for user input
    def prompt(self):
        while True:
            try:
                s = input('calc > ')
            except EOFError:
                break
            if not s:
                continue
            result = self.parser.parse(s)
            print(result)

if __name__ == "__main__":
    m = calculatorParser()
    m.build()
    m.prompt()
