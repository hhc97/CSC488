#!/usr/bin/env python3

import argparse
from ply import lex

# List of token names. This is always required
tokens = [
    'NUMBER',
    'ID',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LESS',
    'LESSEQ',
    'GREATER',
    'GREATEREQ',
    'EQOP',
    'NEQ',
    'AND',
    'BANG',
    'SEMICOL',
    'PERIOD',
    'COMMA',
    'EQ',
    'LPAREN',
    'RPAREN',
    'LBRACK',
    'RBRACK',
    'LBRACE',
    'RBRACE'
]

# Reserved words which should not match any IDs
reserved = {
    'class' : 'CLASS',
    'public' : 'PUBLIC',
    'static' : 'STATIC',
    'extends' : 'EXTENDS',
    'void' : 'VOID',
    'int' : 'INT',
    'boolean' : 'BOOLEAN',
    'main' : 'MAIN',
    'true' : 'TRUE',
    'false' : 'FALSE',
    'this' : 'THIS',
    'new' : 'NEW',
    'null' : 'NULL',
    'String' : 'STRING',
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'return' : 'RETURN'
}

# Add reserved names to list of tokens
tokens += list(reserved.values())

class MiniJavaLexer():

    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'

    # Regular expression rule with some action code
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_LESS = r'\<'
    t_LESSEQ = r'\<='
    t_GREATER = r'\>'
    t_GREATEREQ = r'\>='
    t_EQOP = r'\=='
    t_NEQ = r'\!='
    t_AND = r'\&&'
    t_BANG = r'\!'
    t_SEMICOL = r';'
    t_PERIOD = r'\.'
    t_COMMA = r','
    t_EQ = r'\='
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_LBRACK = r'\['
    t_RBRACK = r'\]'

    # A regular expression rule with some action code
    def t_NUMBER(self, t):
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
if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Take in the miniJava source code and perform lexical analysis.')
    parser.add_argument('FILE', help="Input file with miniJava source code")
    args = parser.parse_args()

    f = open(args.FILE, 'r')
    data = f.read()
    f.close()

    m = MiniJavaLexer()
    m.build()
    m.test(data)
