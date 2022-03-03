#!/usr/bin/env python3

from tinyJavaSymbolTable import SymbolTable, ParseError
import tinyJavaAST as ast

class TypeChecker(object):

    def typecheck(self, node, st=None):
        method = 'check_' + node.__class__.__name__
        return getattr(self, method, self.generic_typecheck)(node, st)

    def generic_typecheck(self, node, st=None):
        print(node)
        if node is None:
            return ''
        else:
            return ''.join(self.typecheck(c, st) for c_name, c in node.children())

    def eq_type(self, t1, t2):
        """
        Helper function to check if two given type node is that of the
        same type. Precondition is that both t1 and t2 are that of class Type
        """
        if not isinstance(t1, ast.Type) or not isinstance(t2, ast.Type):
            raise ParseError("eq_type invoked on non-type objects")
        return t1.name == t2.name

    def check_AssignStmt(self, node, st):

        var_type = st.lookup_variable(node.name, node.coord)
        expr_type = self.typecheck(node.expr, st)
        if not self.eq_type(var_type, expr_type):
            raise ParseError("Variable \"" + node.name + "\" has the type",
                             var_type.name, "but is being assigned the type",
                             expr_type.name)

        return expr_type

    def check_BinOp(self, node, st):
        """
        NOTE
        You should also check if the type of the left and right operation
        makes sense in the context of the operator (ie., you should not be
        able to add/subtract/multiply/divide strings or booleans). In this
        example, it only checks if the left and right expressions are of the
        same type, but that won't be sufficient for your project.
        """

        left_type = self.typecheck(node.left, st)
        right_type = self.typecheck(node.right, st)
        if not self.eq_type(left_type, right_type):
            raise ParseError("Left and right expressions are of different type", node.coord)

        if node.op in ['+', '-', '*', '/']:
            return ast.Type("int")

        return ast.Type("boolean")

    def check_Constant(self, node, st):
        """
        Returns the type of the constant. If the constant refers to
        some kind of id, then we need to find if the id has been declared.
        """
        if self.eq_type(node.type, ast.Type('id')):
            return st.lookup_variable(node.value, node.coord)
        return node.type

    def check_DeclStmt(self, node, st):
        st.declare_variable(node.name, node.type, node.coord)
        if node.expr is not None:
            expr_type = self.typecheck(node.expr, st)
            if not self.eq_type(expr_type, node.type):
                raise ParseError("Mismatch of declaration type", node.coord)

        return node.type

    def check_DeclStmt(self, node, st):
        st.declare_variable(node.name, node.type, node.coord)
        if node.expr is not None:
            expr_type = self.typecheck(node.expr, st)
            if not self.eq_type(expr_type, node.type):
                raise ParseError("Mismatch of declaration type", node.coord)

        return node.type

    def check_Formal(self, node, st):
        st.declare_variable(node.name, node.type, node.coord)
        return node.type

    def check_FuncCall(self, node, st):
        method = st.lookup_method(node.name ,node.coord)

        if len(method.params or []) != len(node.args or []):
            raise ParseError("Argument length mismatch with method", node.coord)

        for i, arg in enumerate(node.args or []):
            arg_type = self.typecheck(arg)
            if not self.eq_type(arg_type, method.params[i].type):
                raise ParseError("Argument type mismatch with method parameter", node.coord)

        return method.ret_type

    def check_IfStmt(self, node, st):
        """
        Check if the condition expression is a boolean type, then
        recursively typecheck all of if statement body.

        Note that most of the programming languages, such as C, Java, and
        Python, all accepts ints/floats for conditions as well. That is
        something you should consider for your project.
        """

        cond_type = self.typecheck(node.cond, st)
        if not self.eq_type(ast.Type('boolean'), cond_type):
            raise ParseError("If statement requires boolean as its condition", node.coord)

        if node.true_body is not None:
            st.push_scope()
            self.typecheck(node.true_body, st)
            st.pop_scope()
        if node.false_body is not None:
            st.push_scope()
            self.typecheck(node.false_body, st)
            st.pop_scope()

        return None

    def check_MethodDecl(self, node, st):

        # Go through the parameters
        for param in node.params:
            self.typecheck(param, st)

        st.push_scope()

        # Go through the method body and type check each statements
        if node.body is not None:
            self.typecheck(node.body, st)

        # Check if the type of the return statement matches the return type
        # of the method
        ret_stmt_type = self.typecheck(node.ret_stmt, st)
        if not self.eq_type(ret_stmt_type, node.ret_type):
            raise ParseError("Mismatch of return type within method \"" +
                             node.name + "\"", node.coord)

        st.pop_scope()

        st.declare_method(node.name, node, node.coord)

        return ret_stmt_type

    def check_ParamList(self, node, st):
        """
        Add all of the parameters to the symbol table
        """
        # Alternatively, you could have a separate check method for
        # "Formal" class, instead of declaring them as a variable here.
        for param in node.params:
            st.declare_variable(param.name, param.type, param.coord)
        return None

    def check_Program(self, node, st=None):
        """
        Generate global symbol table. Recursively typecheck its classes and
        add its class symbol table to itself.
        """
        # Generate global symbol table
        global_st = SymbolTable()

        self.typecheck(node.statements, global_st)

        return global_st

    def check_RetStmt(self, node, st):
        return self.typecheck(node.expr, st)

    def check_StmtList(self, node, st):
        """
        Iterate through all the statements and perform typecheck on them.
        """
        for stmt in node.stmt_lst:
            self.typecheck(stmt, st)

        # List itself does not have any type
        return None

    def check_Type(self, node, st):
        return node
