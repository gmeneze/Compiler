#!/usr/bin/python
"""
parser.py (c) 2016 gmeneze@ncsu.edu, MIT licence
Part of project for course CSC 512: Compiler Construction
http://people.engr.ncsu.edu/xshen5/csc512_fall2016/projects/Scanner.html
USAGE: 
    python scanner.py <input_file>
OUTPUT:
    generates an output file with name obtained by appending "_gen" to the input file.
    This generated file should contain code which produces the same output as the original input file when compiled and executed.
"""

from __future__ import division,print_function
import Scanner, sys,re,traceback,random, operator, string, time
sys.dont_write_bytecode=True

class Parser(object o):
    def program(scanner):
        # '' is interpreted as eof 
        token = token_lookahead(self, 1)
        if token['value'] == '':
            return
        elif token['value'] in ["int", "void", "binary", "decimal"]:
            if token['type'] == Scanner.TOKEN_TYPES.IDENTIFIER:
                return program_z(scanner)
        else
            raiseError



if __name__ == '__main__':
    if len(sys.argv) != 2:
       sys.exit()
    filename = sys.argv[1]
    scanner = Scanner(filename)





