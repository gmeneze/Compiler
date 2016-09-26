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

## Consume every T in a rule in a NT

from __future__ import division,print_function
from Scanner import Scanner, Token, TOKEN_TYPES
import sys,re,traceback,random, operator, string, time
sys.dont_write_bytecode=True

class Parser(object o):
    def program(scanner):
        # '' is interpreted as eof 
        lookahead = scanner.token_lookahead(1)
        if lookahead['value'] == '':
            return True
        elif lookahead['value'] in ['int', 'void', 'binary', 'decimal']:
            scanner.get_next_token()
            if scanner.get_next_token() == TOKEN_TYPES.IDENTIFIER:
                return self.program_z(scanner)
        else
            print("Error in Parser : Non-terminal: <program> : Invalid token")
            return False

    def program_z(scanner):
        lookahead = scanner.token_lookahead(1) 
        if lookahead['value'] in ['[', ';',',']:
            return self.data_decls_new(scanner)
        elif lookahead['value'] == '(':
            return self.func_list_new(scanner)

    def func_list(scanner):
        lookahead = scanner.token_lookahead(1) 
        if lookahead['value'] in ['int', 'void', 'binary', 'decimal']:
            if self.func(scanner):
                return self.func_list(scanner)
            else:
                print("Error in Parser : Non-terminal: <func_list> : Error from <func>")
                return False
        else:
            return True

    def func_list_new(scanner):
        lookahead = scanner.token_lookahead(1) 
        if lookahead['value'] == '(':
            if self.func_decl_new(scanner):
                if self.func_z(scanner):
                    return func_list(scanner)
                else:
                    print("Error in Parser : Non-terminal: <func_list_new> : Error from <func_z>")
                    return False
            else:
                print("Error in Parser : Non-terminal: <func_list_new> : Error from <func_decl_new>")
                return False
        else:
            print("Error in Parser: Non-terminal: <func_list_new> : Invalid token")
            return False

    def func(scanner):
        lookahead = scanner.token_lookahead(1) 
        if lookahead['value'] in ['int', 'void', 'binary', 'decimal']:
            if self.func_decl(scanner):
                return func_z(scanner)
            else:
                print("Error in Parser : Non-terminal: <func> : Error from <func_decl>")
                return False               
        else:
            print("Error in Parser: Non-terminal: <func> : Invalid token")
            return False             

    def func_z(scanner):
        lookahead = scanner.token_lookahead(1) 
        if lookahead['value'] == ';':
            scanner.get_next_token()
            return True
        elif lookahead['value'] == '{':
            scanner.get_next_token()
            if data_decls(scanner):
                if statements(scanner):
                    if scanner.get_next_token() == '}':
                        return True
                    else:
                        print("Error in Parser: Non-terminal: <func_z> : Invalid token")
                        return False                         
                else:
                    print("Error in Parser: Non-terminal: <func_z> : Error from <statements>")
                    return False  
            else:
                print("Error in Parser: Non-terminal: <func_z> : Error from <data_decls>")
                return False  
        else:
             print("Error in Parser: Non-terminal: <func_z> : Invalid token")
            return False             

    

if __name__ == '__main__':
    if len(sys.argv) != 2:
       sys.exit()
    filename = sys.argv[1]
    scanner = Scanner(filename)





