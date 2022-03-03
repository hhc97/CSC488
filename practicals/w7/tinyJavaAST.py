#!/usr/bin/env python3

import sys
from tinyJavaSymbolTable import SymbolTable

class Node(object):
    """
    Abstract base class for AST nodes

    Things to implement:
        __init__: Initialize attributes / children

        children: Method to return list of children. Alternatively, you can
                  look into __iter__ method, which allow nodes to be
                  iterable.
    """

    def children(self):
        """
        A sequence of all children that are Nodes
        """
        pass

    # Set of attributes for a given node
    attr_names = ()

class AssignStmt(Node):
    def __init__(self, name, expr, coord=None):
        self.name = name
        self.expr = expr
        self.coord = coord

    def children(self):
        nodelist = []
        if self.expr is not None:
            nodelist.append(('expr', self.expr))
        return tuple(nodelist)

    attr_names = ('name', )

class BinOp(Node):
    def __init__(self, op, left, right, coord=None):
        self.op = op
        self.left = left
        self.right = right
        self.coord = coord

    def children(self):
        nodelist = []
        if self.left is not None:
            nodelist.append(('left', self.left))
        if self.right is not None:
            nodelist.append(('right', self.right))
        return tuple(nodelist)

    attr_names = ('op', )

class Constant(Node):
    def __init__(self, type, value, coord=None):
        self.type = Type(type)
        self.value = value
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    attr_names = ('type', 'value', )

class DeclStmt(Node):
    def __init__(self, name, type, expr=None, coord=None):
        self.name = name
        self.type = type
        self.expr = expr
        self.coord = coord

    def children(self):
        nodelist = []
        if self.type is not None:
            nodelist.append(('type', self.type))
        if self.expr is not None:
            nodelist.append(('expr', self.expr))
        return tuple(nodelist)

    attr_names = ('name', )

class Formal(Node):
    def __init__(self, name, type, coord=None):
        self.name = name
        self.type = type
        self.coord = coord

    def children(self):
        nodelist = []
        if self.type is not None:
            nodelist.append(('type', self.type))
        return tuple(nodelist)

    attr_names = ('name', )

class FuncCall(Node):
    def __init__(self, name, args, coord=None):
        self.name = name
        self.args = args
        self.coord = coord

    def children(self):
        nodelist = []
        for i, arg in enumerate(self.args or []):
            nodelist.append(('arg[%d]' % i, arg))
        return tuple(nodelist)

    attr_names = ('name', )


class IfStmt(Node):
    def __init__(self, cond, true_body, false_body, coord=None):
        self.cond = cond
        self.true_body = true_body
        self.false_body = false_body

    def children(self):
        nodelist = []
        if self.cond is not None:
            nodelist.append(('cond', self.cond))
        if self.true_body is not None:
            nodelist.append(('true_body', self.true_body))
        if self.false_body is not None:
            nodelist.append(('false_body', self.false_body))
        return tuple(nodelist)

    attr_names = ()

class MethodDecl(Node):
    def __init__(self, name, ret_type, params, body, ret_stmt, coord=None):
        self.name = name
        self.ret_type = ret_type
        self.params = params
        self.body = body
        self.ret_stmt = ret_stmt
        self.coord = coord

    def children(self):
        nodelist = []
        if self.ret_type is not None:
            nodelist.append(('ret_type', self.ret_type))
        for i, param in enumerate(params or []):
            nodelist.append(('param[%d]' % i, param))
        if self.body is not None:
            nodelist.append(('body', self.body))
        if self.ret_stmt is not None:
            nodelist.append(('ret_stmt', self.ret_stmt))
        return tuple(nodelist)

    attr_names = ('name', )

class Program(Node):
    def __init__(self, statements, coord=None):
        self.statements = statements

    def children(self):
        nodelist = []
        if self.statements is not None:
            nodelist.append(('stmtlst', self.statements))
        return tuple(nodelist)

    attr_names = ()

class RetStmt(Node):
    def __init__(self, expr, coord=None):
        self.expr = expr
        self.coord = coord

    def children(self):
        nodelist = []
        if self.expr is not None:
            nodelist.append(('expr', self.expr))
        return tuple(nodelist)

    attr_names = ()

class StmtList(Node):
    def __init__(self, stmt_lst, coord=None):
        self.stmt_lst = stmt_lst

    def children(self):
        nodelist = []
        for i, stmt in enumerate(self.stmt_lst or []):
            nodelist.append(('stmt[%d]' % i, stmt))
        return nodelist

    attr_names = ()

class Type(Node):
    def __init__(self, name, coord=None):
        self.name = name
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    attr_names = ('name', )
