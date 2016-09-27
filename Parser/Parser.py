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
    def program(self, scanner):
        # '' is interpreted as eof 
        lookahead = scanner.token_lookahead(1)
        if lookahead['value'] == '':
            return True
        elif lookahead['value'] in ['int', 'void', 'binary', 'decimal']:
            scanner.get_next_token()
            if scanner.get_next_token()['type'] == TOKEN_TYPES.IDENTIFIER:
                return self.program_z(scanner)
        else
            print("Error in Parser : Non-terminal: <program> : Invalid token")
            return False

    def program_z(self, scanner):
        lookahead = scanner.token_lookahead(1) 
        if lookahead['value'] in ['[', ';',',']:
            return self.data_decls_new(scanner)
        elif lookahead['value'] == '(':
            return self.func_list_new(scanner)

    def func_list(self, scanner):
        lookahead = scanner.token_lookahead(1) 
        if lookahead['value'] in ['int', 'void', 'binary', 'decimal']:
            if self.func(scanner):
                return self.func_list(scanner)
            else:
                print("Error in Parser : Non-terminal: <func_list> : Error from <func>")
                return False
        else:
            return True

    def func_list_new(self, scanner):
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

    def func(self, scanner):
        lookahead = scanner.token_lookahead(1) 
        if lookahead['value'] in ['int', 'void', 'binary', 'decimal']:
            if self.func_decl(scanner):
                return self.func_z(scanner)
            else:
                print("Error in Parser : Non-terminal: <func> : Error from <func_decl>")
                return False               
        else:
            print("Error in Parser: Non-terminal: <func> : Invalid token")
            return False             

    def func_z(self, scanner):
        lookahead = scanner.token_lookahead(1) 
        if lookahead['value'] == ';':
            scanner.get_next_token()
            return True
        elif lookahead['value'] == '{':
            scanner.get_next_token()
            if self.data_decls(scanner):
                if self.statements(scanner):
                    if scanner.get_next_token()['value'] == '}':
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

    def func_decl(self, scanner):
         lookahead = scanner.token_lookahead(1)
         if lookahead['value'] in ['int', 'void', 'binary', 'decimal']:
            scanner.get_next_token()
            if scanner.get_next_token()['type'] == TOKEN_TYPES.IDENTIFIER:
                if scanner.get_next_token()['value'] == '(':
                    if parameter_list(scanner):
                        if scanner.get_next_token()['value'] == ')':
                            return True
                        else:
                            print("Error in Parser: Non-terminal: <func_decl> : Invalid token")
                            return False 
                    else:
                        print("Error in Parser: Non-terminal: <func_decl> : Error from <parameter_list>")
                        return False                        
                else:
                    print("Error in Parser: Non-terminal: <func_decl> : Invalid token")
                    return False   
            else:
                print("Error in Parser: Non-terminal: <func_decl> : Invalid token")
                return False 
        else:
            print("Error in Parser: Non-terminal: <func_decl> : Invalid token")
            return False                                        


    def func_decl_new(self, scanner):
        lookahead = scanner.token_lookahead(1)
        if lookahead['value'] == '(':
            scanner.get_next_token()
            if parameter_list(scanner):
                if scanner.get_next_token()['value'] == ')':
                    return True
                else:
                    print("Error in Parser: Non-terminal: <func_decl_new> : Invalid token")
                    return False 
            else:
                print("Error in Parser: Non-terminal: <func_decl_new> : Error from <parameter_list>")
                return False                                    
        else:
            print("Error in Parser: Non-terminal: <func_decl_new> : Invalid token")
            return False             


    def type_name(self, scanner):
        lookahead = scanner.token_lookahead(1)
        if lookahead['value'] in ['int', 'void', 'binary', 'decimal']:
            scanner.get_next_token()
        else:
            print("Error in Parser: Non-terminal: <type_name> : Invalid token")
            return False 
     
    def parameter_list(self, scanner):
        lookahead = scanner.token_lookahead(1)
        if lookahead['value'] == 'void':
            scanner.get_next_token()
            if parameter_list_z(scanner):
                return True
            else:
                print("Error in Parser: Non-terminal: <parameter_list> : Error from <non_empty_list_prime>")
                return False
        elif lookahead['value'] == 'int':
            scanner.get_next_token()
            if scanner.get_next_token()['type'] == TOKEN_TYPES.IDENTIFIER:
                if non_empty_list_prime(scanner):
                    return True
                else:
                    print("Error in Parser: Non-terminal: <parameter_list> : Error from <non_empty_list_prime>")
                    return False
            else:
                print("Error in Parser: Non-terminal: <parameter_list> : Error from <non_empty_list_prime>")
                return False               
        elif lookahead['value'] == 'binary':
            scanner.get_next_token()
            if scanner.get_next_token()['type'] == TOKEN_TYPES.IDENTIFIER:
                if non_empty_list_prime(scanner):
                    return True
                else:
                    print("Error in Parser: Non-terminal: <parameter_list> : Error from <non_empty_list_prime>")
                    return False
            else:
                print("Error in Parser: Non-terminal: <parameter_list> : Error from <non_empty_list_prime>")
                return False 
        elif lookahead['value'] == 'decimal':
            scanner.get_next_token()
            if scanner.get_next_token()['type'] == TOKEN_TYPES.IDENTIFIER:
                if non_empty_list_prime(scanner):
                    return True
                else:
                    print("Error in Parser: Non-terminal: <parameter_list> : Error from <non_empty_list_prime>")
                    return False
            else:
                print("Error in Parser: Non-terminal: <parameter_list> : Error from <non_empty_list_prime>")
                return False 
        else:
            return True   



    def parameter_list_z(self, scanner):
        lookahead = scanner.token_lookahead(1)
        if lookahead['type'] == TOKEN_TYPES.IDENTIFIER:
            scanner.get_next_token()
            if non_empty_list_prime(scanner):
                return True
            else:
                print("Error in Parser: Non-terminal: <parameter_list_z> : Error from <non_empty_list_prime>")
                return False   
        else:
            return True  

    def non_empty_list(self, scanner):
        lookahead = scanner.token_lookahead(1)
        if lookahead['type'] in ['int', 'void', 'binary', 'void']:
            scanner.get_next_token()
            if scanner.get_next_token()['type'] == TOKEN_TYPES.IDENTIFIER:
                if self.non_empty_list_prime(scanner):
                    return True
                else:
                    print("Error in Parser: Non-terminal: <non_empty_list> : Error from <non_empty_list_prime>")
                    return False 
            else:
                print("Error in Parser: Non-terminal: <non_empty_list> : Invalid token")
                return False  
        else:
            print("Error in Parser: Non-terminal: <non_empty_list> : Invalid token")
            return False   

    def non_empty_list_prime(self, scanner):
        lookahead = scanner.token_lookahead(1)
        if lookahead['value'] == ',':
            scanner.get_next_token()
            if scanner.get_next_token()['type'] ==  TOKEN_TYPES.IDENTIFIER:
                if self.non_empty_list_prime(scanner):
                    return True
                else:
                    print("Error in Parser: Non-terminal: <non_empty_list_prime> : Error from <non_empty_list_prime>")
                    return False 
            else:
                print("Error in Parser: Non-terminal: <non_empty_list_prime> : Invalid token")
                return False                                                               
        else:
            return True   


    def data_decls(self, scanner):
        lookahead = scanner.token_lookahead(1)
        if lookahead['value'] in ['int', 'void', 'binary', 'void']:
            scanner.get_next_token()
            if self.id_list(scanner):
                if scanner.get_next_token()['value'] == ';':
                    scanner.get_next_token()
                    if self.data_decls(scanner):
                        return True
                    else:
                        print("Error in Parser: Non-terminal: <data_decls> : Error from <data_decls>")
                        return False                        
                else:
                    print("Error in Parser: Non-terminal: <data_decls> : Invalid token")
                    return False 
            else:
                print("Error in Parser: Non-terminal: <data_decls> : Error from <id_list>")
                return False                                                               
        else:
            return True 


    def data_decls_new(self, scanner):
        lookahead = scanner.token_lookahead(1)
        if lookahead['value'] in ['[', ';', ','] :
            if id_z(scanner):
                if id_list_prime(scanner):
                    if scanner.get_next_token()['value'] == ';':
                        if data_or_func_decl(scanner):
                            return True
                        else:
                            print("Error in Parser: Non-terminal: <data_decls_new> : Error from <data_or_func_decl>")
                            return False                            
                    else: 
                        print("Error in Parser: Non-terminal: <data_decls_new> : Invalid token")
                        return False        
                else:
                    print("Error in Parser: Non-terminal: <data_decls_new> : Error from <id_list_prime>")
                    return False                     
            else:
                print("Error in Parser: Non-terminal: <data_decls_new> : Error from <id_z>")
                return False  
        else:
            print("Error in Parser: Non-terminal: <data_decls_new> : Invalid token")
            return False           

    def data_or_func_decl(self, scanner):
        lookahead = scanner.token_lookahead(1)
        if lookahead['value'] in ['int', 'void', 'binary', 'void']:
            scanner.get_next_token()
            if scanner.get_next_token()['type'] == TOKEN_TYPES.IDENTIFIER:
                if data_or_func_z(scanner):
                   return True
                else:
                    print("Error in Parser: Non-terminal: <data_or_func_decl> : Error from <data_or_func_z>")
                    return False  
            else:
                print("Error in Parser: Non-terminal: <data_or_func_decl> : Invalid token")
                return False 
        else:
            return True

     def data_or_func_decl_z(self, scanner):
        lookahead = scanner.token_lookahead(1)
        if lookahead['value'] in ['[', ';', ',']:
            if data_decls_new(scanner):
                return True
            else:
                print("Error in Parser: Non-terminal: <data_or_func_decl_z> : Error from <data_decls_new>")
                return False                
        elif lookahead['value'] == '(':
            if func_list_new(scanner):
                return True
            else:
                print("Error in Parser: Non-terminal: <data_or_func_decl_z> : Error from <func_list_new>")
                return False 
        else:
             print("Error in Parser: Non-terminal: <data_or_func_decl_z> : Invalid Token")
            return False            


     def data_or_func_decl_z(self, scanner):
        lookahead = scanner.token_lookahead(1)
        if lookahead['value'] in ['[', ';', ',']:
            if data_decls_new(scanner):
                return True
            else:
                print("Error in Parser: Non-terminal: <data_or_func_decl_z> : Error from <data_decls_new>")
                return False                
        elif lookahead['value'] == '(':
            if func_list_new(scanner):
                return True
            else:
                print("Error in Parser: Non-terminal: <data_or_func_decl_z> : Error from <func_list_new>")
                return False 
        else:
             print("Error in Parser: Non-terminal: <data_or_func_decl_z> : Invalid Token")
            return False  

    def id_list(self, scanner):
        lookahead = scanner.token_lookahead(1)
        if lookahead['type'] ==  TOKEN_TYPES.IDENTIFIER:
            if self.id(scanner):
                if self.id_list_prime(scanner):
                    return True
                else:
                    print("Error in Parser: Non-terminal: <id_list> : Error from <id_list_prime>")
                    return False 
            else:
                print("Error in Parser: Non-terminal: <id_list> : Error from <id>")
                return False
        else:
            print("Error in Parser: Non-terminal: <id_list> : Invalid Token")
            return False                           
                                       

    def id_list_prime(self, scanner):
        lookahead = scanner.token_lookahead(1)
        if lookahead['value'] == ',':
            scanner.get_next_token()
            if self.id(scanner):
                return True
            else:
                print("Error in Parser: Non-terminal: <id_list_prime> : Error from <id_list_prime>")
                return False 
        else:
            return True               

    def data_decls(self, scanner):


    def data_decls_new(self, scanner):

    def data_or_func_decl(self, scanner):

    def data_or_func_decl_z(self, scanner):

    def id_list(self, scanner):

    def id_list_prime(self, scanner):

    def id(self, scanner):

    def id_z(self, scanner):

    def block_statements(self, scanner):

    def statements(self, scanner):

    def statement(self, scanner):

    def statement_z(self, scanner):

    def assignment(self, scanner):

    def func_call(self, scanner):

if __name__ == '__main__':
    if len(sys.argv) != 2:
       sys.exit()
    filename = sys.argv[1]
    scanner = Scanner(filename)





