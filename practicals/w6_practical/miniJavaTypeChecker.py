#!/usr/bin/env python3

from miniJavaSymbolTable import SymbolTable, GlobalSymbolTable, ClassSymbolTable, ParseError
import miniJavaAST as ast

class TypeChecker(object):
    """
    Uses the same visitor pattern as ast.NodeVisitor, but modified to
    perform type checks, as well as to generate the symbol table.

    This TypeChecker is setup in a way that Program and ClassDecl visitors
    will return its symbol table, while other visitor functions will
    return the type of the associated object. This is so that we can use
    the return value of typecheck directly to check its type. If the object
    is not associated with either symbol table or a type, then it will return
    None.

    Alternatively, you could implement a method which returns the
    type of the object in question into the Node object.

    Additionally, this is not the only way of implementing visitor either.
    You could implement visitor design pattern straight into Node object
    rather than having a separate visitor.

    Finally, IR (Intermediate Representation) generators use the similar
    visitor pattern, and it may also require the symbol table which is
    being generated here. You should bare this in mind for sprint2 as you
    design your compiler to support type-checking and IR generator.

    NOTE: This Typechecker is as incomplete as the miniJava Parser -- meaning
          lack of features from parsers will impact this typechecker as well!
          (i.e., no method call, can only declare one method at a time, etc...)
    """

    def typecheck(self, node, st=None):
        method = 'check_' + node.__class__.__name__
        return getattr(self, method, self.generic_typecheck)(node, st)

    def generic_typecheck(self, node, st=None):
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

    def check_ClassDecl(self, node, st):

        # Generate class symbol table
        class_st = ClassSymbolTable(node.name, node.extend)

        # If there is a class variable declared, add to the symbol table
        var = node.var_decl
        if var is not None:
            class_st.declare_variable(var.name, var.type, var.coord)

        # If there is a method declared, add to the symbol table and recursively
        # typecheck the method as well.
        # Note that currently, the grammar only specifies a single method
        # per class -- however, this can be extended to support multiple
        # methods. Similar can be said for Program visitor with multiple
        # classes.
        method = node.method_decl
        if method is not None:
            class_st.declare_method(method.name, method, method.coord)
            self.typecheck(method, class_st)

        return class_st

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
            self.typecheck(node.true_body, st)
        if node.false_body is not None:
            self.typecheck(node.false_body, st)

        return None

    def check_MethodDecl(self, node, st):

        # Go through the parameters
        if node.params is not None:
            self.typecheck(node.params, st)
        # Go through the method body and type check each statements
        if node.body is not None:
            self.typecheck(node.body, st)

        # Check if the type of the return statement matches the return type
        # of the method
        ret_stmt_type = self.typecheck(node.ret_stmt, st)
        if not self.eq_type(ret_stmt_type, node.ret_type):
            raise ParseError("Mismatch of return type within method \"" +
                             node.name + "\"", node.coord)

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
        global_st = GlobalSymbolTable()

        # Iterate through the declared classes, perform typecheck on them
        # and add them to the global symbol table
        for (child_name, child) in node.children():
            class_st = self.typecheck(child, global_st)
            global_st.declare_class(class_st.class_name, class_st, child.coord)

        return global_st

    def check_RetStmt(self, node, st):
        return self.typecheck(node.expr, st)

    def check_StmtList(self, node, st):
        """
        Iterate through all the statements and perform typecheck on them.
        StmtList acts similarily to a new scope -- it should push additional
        scope to the scope_stack and pop the scope when done.
        """
        st.push_scope()
        for stmt in node.stmt_lst:
            self.typecheck(stmt, st)
        st.pop_scope()

        # List itself does not have any type
        return None

    def check_Type(self, node, st):
        return node

    def check_UnaryOp(self, node, st):
        """
        NOTE
        Similar to BinOp, you should check if the unary operator is
        applicable with the type returned by the expression
        (i.e., '-' could only make sense if the expression is an integer)
        """
        return self.typecheck(node.expr, st)

    def check_WhileStmt(self, node, st):
        """
        First, check if the condition returns the type boolean.
        Then, push another scope into the scope stack and perform typecheck
        within the while statement body.
        """

        cond_type = self.typecheck(node.cond, st)
        if not self.eq_type(ast.Type('boolean'), cond_type):
            raise ParseError("While statement requires boolean as its condition", node.coord)

        if node.body is not None:
            self.typecheck(node.body, st)

        return None
