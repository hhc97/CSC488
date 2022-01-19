#!/usr/bin/env python3

import argparse
from ply import lex

# List of token names. This is always required
tokens = [
    'DECIMAL',
    'ID',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'SEMICOL',
    'EQ',
    'LPAREN',
    'RPAREN',

    # TODO: Add additional tokens here
]

# Reserved words which should not match any IDs
reserved = {
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',
    'while' : 'WHILE',

    # TODO: Add additional reserved words here
}

# Add reserved names to list of tokens
tokens += list(reserved.values())

class miniJavaLexer():

    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'

    # Regular expression rule with some action code
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_SEMICOL = r';'
    t_EQ = r'\='
    t_LPAREN = r'\('
    t_RPAREN = r'\)'

    # TODO: Add simple regex rule for tokens you have added
    # Bare in mind that variable name for these rules should always be:
    #       t_{TNAME}
    # where TNAME is the name of the token you want to specify.
    # Also bare in mind that you may need to add "\" infront of some characters,
    # since they may be used as part of the regex pattern

    # A regular expression rule with some action code
    def t_DECIMAL(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = reserved.get(t.value, 'ID') # Check for reserved words
        return t

    # Define a rule so we can track line numbers. DO NOT MODIFY
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Error handling rule. DO NOT MODIFY
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer. DO NOT MODIFY
    def build(self, **kwargs):
        self.tokens = tokens
        self.lexer = lex.lex(module=self, **kwargs)

    # Test the output. DO NOT MODIFY
    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)

# Main function. DO NOT MODIFY
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Take in the miniJava source code and perform lexical analysis.')
    parser.add_argument('FILE', help="Input file with miniJava source code")
    args = parser.parse_args()

    f = open(args.FILE, 'r')
    data = f.read()
    f.close()

    m = miniJavaLexer()
    m.build()
    m.test(data)
