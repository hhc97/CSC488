#!/usr/bin/env python3

import argparse
from tinyJavaParser import TinyJavaParser
from tinyJavaSymbolTable import SymbolTable
from tinyJavaTypeChecker import TypeChecker
from tinyJavaIRGen import IRGen

import tinyJavaAST as ast

if __name__ == "__main__":

    # Python module "argparse" allows you to easily add commandline flags
    # to your program, which can help with adding debugging options, such
    # as '--verbose' and '--print-ast' as described below.
    #
    # Of course, this is entirely optional and not necessary, as long as
    # the compiler functions correctly.
    argparser = argparse.ArgumentParser(description='Take in the miniJava source code and compile it')
    argparser.add_argument('FILE', help="Input file")
    argparser.add_argument('-p', '--parse-only', action='store_true', help="Stop after scanning and parsing the input")
    argparser.add_argument('-t', '--typecheck-only', action='store_true', help="Stop after typechecking")
    argparser.add_argument('-v', '--verbose', action='store_true', help="Provides additional output")
    args = argparser.parse_args()

    # Prints additional output if the flag is set
    if args.verbose:
        print("* Reading file " + args.FILE + "...")

    f = open(args.FILE, 'r')
    data = f.read()
    f.close()

    if args.verbose:
        print("* Scanning and Parsing...")

    # Build and runs the parser to get AST
    parser = TinyJavaParser()
    root = parser.parse(data)

    # If user asks to quit after parsing, do so.
    if args.parse_only:
        quit()

    if args.verbose:
        print("* Typechecking...")

    typechecker = TypeChecker()
    typechecker.typecheck(root)

    if args.verbose:
        print("* Generating IR...")

    ir_generator = IRGen()
    ir_generator.generate(root)
    ir_generator.print_ir()
