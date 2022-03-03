#!/usr/bin/env python3

class IRGen(object):
    """
    Uses the same visitor pattern as TypeChecker. It is modified to
    generate 3AC (Three Address Code) in a simple string.

    Bare in mind that this is for demonstration purpose only! For your
    actual project, you would want to generate some sort of objects rather
    than plain string. However, this should help you think about what you
    might want/need to do to convert your AST to your IR of choice.

    As mentioned in the tutorial, you are free to choose which IR you
    want to generate. I suggest you look into different optimization,
    as well as think about how your IR of choice will translate to your
    target language, since you would need to argue why your IR of choice
    makes sense for Sprint2.
    """

    def __init__(self):
        """
        IR_lst: list of IR code
        register_count: integer to keep track of which register to use
        label_count: similar to register_count, but with labels
        """
        self.IR_lst = []
        self.register_count = 0
        self.label_count = 0

    def generate(self, node):
        """
        Similar to 'typecheck' method from TypeChecker object
        """
        method = 'gen_' + node.__class__.__name__
        return getattr(self, method)(node)

    ################################
    ## Helper functions
    ################################

    def add_code(self, code):
        """
        Add 'code' to the IR_lst with correct spacing
        """
        self.IR_lst.append("    " + code)

    def inc_register(self):
        """
        Increase the register count and return its value for use
        """
        self.register_count += 1
        return self.register_count

    def reset_register(self):
        """
        Can reset the register_count to reuse them
        """
        self.register_count = 0

    def inc_label(self):
        """
        Increase the label count and return its value for use
        """
        self.label_count += 1
        return self.label_count

    def mark_label(self, label):
        """
        Add label mark to IR_lst
        """
        self.IR_lst.append("_L{}:".format(label))

    def print_ir(self):
        """
        Loop through the generated IR code and print them out to stdout
        """
        for ir in self.IR_lst:
            print(ir)

    def gen_AssignStmt(self, node):
        expr = self.generate(node.expr)
        self.add_code("{} := {}".format(node.name, expr))
        self.register_count = 0

    def gen_BinOp(self, node):
        # Left operand
        left = self.generate(node.left)
        # Right operand
        right = self.generate(node.right)

        reg = self.inc_register()
        self.add_code("{} := {} {} {}".format('_t%d' % reg, left, node.op, right))

        return '_t%d' % reg

    def gen_Constant(self, node):
        return node.value

    def gen_DeclStmt(self, node):
        expr = self.generate(node.expr)
        self.add_code("{} := {}".format(node.name, expr))
        self.register_count = 0

    def gen_FuncCall(self, node):

        # Push all of the arguments with "PushParam" function
        args = node.children()
        for (i, arg) in args:
            self.add_code("PushParam %s" % self.generate(arg))

        # Once all of the parameter has been pushed, actually call the function
        self.add_code("FuncCall %s" % node.name)

        # After we're done with the function, remove the spaces reserved
        # for the arguments
        self.add_code("PopParams %d" % len(args))

        reg = self.inc_register()
        self.add_code("{} := ret".format('_t%d' % reg))

        return '_t%d' % reg

    def gen_IfStmt(self, node):
        cond = self.generate(node.cond)

        fbranch_label = self.inc_label()
        tbranch_label = self.inc_label()

        # Skip to the false_body if the condition is not met
        self.add_code("if !({}) goto {}".format(cond, '_L%d' % fbranch_label))
        self.generate(node.true_body)
        # Make sure the statements from false_body is skipped
        self.add_code("goto _L%d" % tbranch_label)

        self.mark_label(fbranch_label)
        self.generate(node.false_body)
        self.mark_label(tbranch_label)

    def gen_MethodDecl(self, node):

        skip_decl = self.inc_label()

        # We want to skip the function code until it is called
        self.add_code("goto _L%d" % skip_decl)

        # Function label
        self.mark_label(node.name)

        # Allocate room for function local variables
        self.add_code("BeginFunc")

        # Actually generate the main body
        self.generate(node.body)
        self.generate(node.ret_stmt)

        # Do any cleanup before jumping back
        self.add_code("EndFunc")

        self.mark_label(skip_decl)

    def gen_Program(self, node):
        for (child_name, child) in node.children():
            self.generate(child)

    def gen_RetStmt(self, node):
        expr = self.generate(node.expr)
        self.add_code("ret := {}".format(expr))

    def gen_StmtList(self, node):
        for stmt in node.stmt_lst:
            self.generate(stmt)
