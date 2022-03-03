#!/usr/bin/env python3

from ply import lex

# List of token names. This is always required
tokens = [
    'NUMBER',
    'ID',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'COMMA',
    'EQOP',
    'NEQ',
    'SEMICOL',
    'EQ',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE'
]

# Reserved words which should not match any IDs
reserved = {
    'int' : 'INT',
    'boolean' : 'BOOLEAN',
    'true' : 'TRUE',
    'false' : 'FALSE',
    'if' : 'IF',
    'else' : 'ELSE',
    'return' : 'RETURN',
    'public' : 'PUBLIC'
}

# Add reserved names to list of tokens
tokens += list(reserved.values())

class TinyJavaLexer():

    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'

    # Regular expression rule with some action code
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_COMMA = r'\,'
    t_EQOP = r'\=='
    t_NEQ = r'\!='
    t_SEMICOL = r';'
    t_EQ = r'\='
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'

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
