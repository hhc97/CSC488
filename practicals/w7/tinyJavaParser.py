#!/usr/bin/env python3

from ply import yacc
from tinyJavaLexer import TinyJavaLexer
import tinyJavaAST as ast

from tinyJavaLexer import tokens

class TinyJavaParser:

    precedence = (
        ('left', 'EQOP', 'NEQ'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE')
    )

    # Let the parser know that symbol "program" is the starting point
    start = 'program'

    def __init__(self):
        """
        Builds the Lexer and Parser
        """
        self.tokens = tokens
        self.lexer = TinyJavaLexer()
        self.lexer.build()
        self.parser = yacc.yacc(module=self)

    def parse(self, data):
        """
        Returns the root (Program) node of the AST, after parsing the file
        """
        return self.parser.parse(data)

    ################################
    ## Program (starting point)
    ################################

    def p_program(self, p):
        '''
        program : stmts_or_empty
        '''
        p[0] = ast.Program(p[1], p.lineno(1))

    ################################
    ## Statements
    ################################

    def p_scope(self, p):
        '''
        scope : LBRACE stmts_or_empty RBRACE
        '''
        p[0] = p[2]

    def p_statements_or_empty(self, p):
        '''
        stmts_or_empty : stmt_lst
                       | empty
        '''
        p[0] = ast.StmtList(p[1], p.lineno(1))

    def p_statement_list(self, p):
        '''
        stmt_lst : stmt_lst stmt
                 | stmt
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_statement(self, p):
        '''
        stmt : decl_stmt
             | assign_stmt
             | if_stmt
             | method_decl
        '''
        p[0] = p[1]

    def p_decl_statement(self, p):
        '''
        decl_stmt : type ID EQ expr SEMICOL
        '''
        p[0] = ast.DeclStmt(p[2], p[1], p[4], p.lineno(2))

    def p_assignment_statement(self, p):
        '''
        assign_stmt : ID EQ expr SEMICOL
        '''
        p[0] = ast.AssignStmt(p[1], p[3], p.lineno(1))

    def p_if_statement(self, p):
        '''
        if_stmt : IF LPAREN expr RPAREN scope ELSE scope
        '''
        p[0] = ast.IfStmt(p[3], p[5], p[7], p.lineno(1))

    def p_if_stmt_no_else(self, p):
        '''
        if_stmt : IF LPAREN expr RPAREN scope
        '''
        p[0] = ast.IfStmt(p[3], p[5], None, p.lineno(1))

    def p_return_statement(self, p):
        '''
        ret_stmt : RETURN expr SEMICOL
        '''
        p[0] = ast.RetStmt(p[2], p.lineno(1))

    ################################
    ## Method Declarations
    ################################

    def p_method_decl(self, p):
        '''
        method_decl : PUBLIC type ID method_param LBRACE stmts_or_empty ret_stmt RBRACE
        '''
        p[0] = ast.MethodDecl(p[3], p[2], p[4], p[6], p[7], p.lineno(1))

    def p_method_param(self, p):
        '''
        method_param : LPAREN formals_or_empty RPAREN
        '''
        p[0] = p[2]

    def p_formals_or_empty(self, p):
        '''
        formals_or_empty : formal_lst
                         | empty
        '''
        if len(p) == 1:
            p[0] = []
        else:
            p[0] = p[1]

    def p_formal_lst(self, p):
        '''
        formal_lst : formal_lst COMMA formal
                   | formal
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_formal(self, p):
        '''
        formal : type ID
        '''
        p[0] = ast.Formal(p[2], p[1], p.lineno(2))

    ################################
    ## Expressions
    ################################

    def p_expr_func_call(self, p):
        '''
        expr : ID LPAREN expr_lst_or_empty RPAREN
        '''
        p[0] = ast.FuncCall(p[1], p[3], p.lineno(1))

    def p_expr_lst_or_empty(self, p):
        '''
        expr_lst_or_empty : expr_lst
                          | empty
        '''
        if len(p) == 1:
            p[0] = []
        else:
            p[0] = p[1]

    def p_expr_lst(self, p):
        '''
        expr_lst : expr_lst COMMA expr
                 | expr
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_expr_binops(self, p):
        '''
        expr : expr PLUS expr
             | expr MINUS expr
             | expr TIMES expr
             | expr DIVIDE expr
             | expr EQOP expr
             | expr NEQ expr
        '''
        p[0] = ast.BinOp(p[2], p[1], p[3], p.lineno(1))

    def p_expr_group(self, p):
        '''
        expr : LPAREN expr RPAREN
        '''
        p[0] = p[2]

    def p_expr_number(self, p):
        '''
        expr : NUMBER
        '''
        p[0] = ast.Constant('int', p[1], p.lineno(1))

    def p_expr_bool(self, p):
        '''
        expr : TRUE
             | FALSE
        '''
        p[0] = ast.Constant('boolean', p[1], p.lineno(1))

    def p_expr_id(self, p):
        '''
        expr : ID
        '''
        p[0] = ast.Constant('id', p[1], p.lineno(1))

    ################################
    ## Types
    ################################

    def p_type(self, p):
        '''
        type : base_type
             | ID
        '''
        p[0] = ast.Type(p[1], p.lineno(1))

    def p_base_type(self, p):
        '''
        base_type : INT
                  | BOOLEAN
        '''
        p[0] = p[1]

    ################################
    ## Misc
    ################################

    # This can be used to handle the empty production, by using 'empty'
    # as a symbol. For example:
    #
    #       optitem : item
    #               | empty
    def p_empty(self, p):
        'empty :'
        pass

    def p_error(self, p):
        print("Syntax error at token", p)
