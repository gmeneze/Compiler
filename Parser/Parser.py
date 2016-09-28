#!/usr/bin/python
"""
parser.py (c) 2016 gmeneze@ncsu.edu, MIT licence
Part of project for course CSC 512: Compiler Construction
http://people.engr.ncsu.edu/xshen5/csc512_fall2016/projects/self.scanner.html
USAGE: 
    python self.scanner.py <input_file>
OUTPUT:
    generates an output file with name obtained by appending "_gen" to the input file.
    This generated file should contain code which produces the same output as the original input file when compiled and executed.
"""

from __future__ import division,print_function
from Scanner import Scanner, Token, TOKEN_TYPES, DEBUG
import sys,re,traceback,random, operator, string, time
sys.dont_write_bytecode=True

class Parser(object):
    def __init__(self, filename):
        self.scanner = Scanner(filename)
        self.variable_count = 0
        self.function_count = 0
        self.statement_count = 0

    def program(self):
        if DEBUG: 
            print("<program> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        # '' is interpreted as eof 
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] == '':
            return True
        elif lookahead['value'] in ['int', 'void', 'binary', 'decimal']:
            self.scanner.get_next_token()
            if self.scanner.get_next_token()['type'] == TOKEN_TYPES.IDENTIFIER:
                if self.program_z():
                    # check if parsing has been completed
                    if self.scanner.get_next_token()['value'] == '': 
                        if DEBUG:
                            print("<program> : return True")
                        return True
                    else:
                        if DEBUG:
                            print("Parsing not completed, error in file") 
                        return False
                else:
                    if DEBUG:
                        print("Error in Parser : Non-terminal: <program> : Error from <program_z>")
                    return False  
            else:
                if DEBUG:
                    print("Error in Parser : Non-terminal: <program> : Invalid token")
                return False                                   
        else:
            if DEBUG:
                print("Error in Parser : Non-terminal: <program> : Invalid token")
            return False

    def program_z(self):
        if DEBUG:
            print("<program_z> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1) 
        if lookahead['value'] in ['[', ';',',']:
            if self.data_decls_new():
                if DEBUG:
                    print("<program_z> : return True")
                return True
            else:
                if DEBUG:
                    print("Error in Parser : Non-terminal: <program_z> : Error from <data_decls_new>")
                return False                 
        elif lookahead['value'] == '(':
            if self.func_list_new():
                if DEBUG:
                    print("<program_z> : return True")
                return True
            else:
                if DEBUG:
                    print("Error in Parser : Non-terminal: <program_z> : Error from <func_list_new>")
                return False         
        else:
            if DEBUG:
                print("Error in Parser : Non-terminal: <program_z> : Invalid token")
            return False                     

    def func_list(self):
        if DEBUG:
            print("<func_list> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1) 
        if lookahead['value'] in ['int', 'void', 'binary', 'decimal']:
            if self.func():
                if self.func_list():
                    if DEBUG:
                        print("<func_list> : return True")
                    return True
                else:
                    if DEBUG:
                        print("Error in Parser : Non-terminal: <func_list> : Error from <func_list>")
                    return False                    
            else:
                if DEBUG:
                    print("Error in Parser : Non-terminal: <func_list> : Error from <func>")
                return False
        else:
            if DEBUG:
                print("<func_list> : return True")
            return True

    def func_list_new(self):
        if DEBUG:
            print("<func_list_new> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1) 
        if lookahead['value'] == '(':
            if self.func_decl_new():
                if self.func_z():
                    if self.func_list():
                        if DEBUG:
                            print("<func_list_new> : return True")
                        return True
                    else:
                        if DEBUG:
                            print("Error in Parser : Non-terminal: <func_list_new> : Error from <func_list>")
                        return False                       
                else:
                    if DEBUG:
                        print("Error in Parser : Non-terminal: <func_list_new> : Error from <func_z>")
                    return False
            else:
                if DEBUG:
                    print("Error in Parser : Non-terminal: <func_list_new> : Error from <func_decl_new>")
                return False
        else:
            if DEBUG:
                print("Error in Parser: Non-terminal: <func_list_new> : Invalid token")
            return False

    def func(self):
        if DEBUG:
            print("<func> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1) 
        if lookahead['value'] in ['int', 'void', 'binary', 'decimal']:
            if self.func_decl():
                if self.func_z():
                    if DEBUG:
                        print("<func> : return True")
                    return True
                else:
                    if DEBUG:
                        print("Error in Parser : Non-terminal: <func> : Error from <func_z>")
                    return False                    
            else:
                if DEBUG:
                    print("Error in Parser : Non-terminal: <func> : Error from <func_decl>")
                return False               
        else:
            if DEBUG:
                print("Error in Parser: Non-terminal: <func> : Invalid token")
            return False             

    def func_z(self):
        if DEBUG:
            print("<func_z> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1) 
        if lookahead['value'] == ';':
            self.scanner.get_next_token()
            if DEBUG:
                print("<func_z> : return True")
            return True
        elif lookahead['value'] == '{':
            self.scanner.get_next_token()
            if self.data_decls():
                if DEBUG:
                    print("glen 1 <func_z> called with input : <%s> " % (self.scanner.token_lookahead(1)))
                if self.statements():
                    if DEBUG:
                        print("glen 2 <func_z> called with input : <%s> " % (self.scanner.token_lookahead(1)))
                    if self.scanner.get_next_token()['value'] == '}':
                        self.function_count = self.function_count + 1
                        if DEBUG:
                            print("<func_z> : return True")
                        return True
                    else:
                        if DEBUG:
                            print("1 Error in Parser: Non-terminal: <func_z> : Invalid token")
                        return False                         
                else:
                    if DEBUG:
                        print("Error in Parser: Non-terminal: <func_z> : Error from <statements>")
                    return False  
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <func_z> : Error from <data_decls>")
                return False  
        else:
            if DEBUG:
                print("2 Error in Parser: Non-terminal: <func_z> : Invalid token")
            return False   

    def func_decl(self):
        if DEBUG:
            print("<func_decl> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] in ['int', 'void', 'binary', 'decimal']:
            self.scanner.get_next_token()
            if self.scanner.get_next_token()['type'] == TOKEN_TYPES.IDENTIFIER:
                if self.scanner.get_next_token()['value'] == '(':
                    if self.parameter_list():
                        if self.scanner.get_next_token()['value'] == ')':
                            if DEBUG:
                                print("<func_decl> : return True")
                            return True
                        else:
                            if DEBUG:
                                print("Error in Parser: Non-terminal: <func_decl> : Invalid token")
                            return False 
                    else:
                        if DEBUG:
                            print("Error in Parser: Non-terminal: <func_decl> : Error from <parameter_list>")
                        return False                        
                else:
                    if DEBUG:
                        print("Error in Parser: Non-terminal: <func_decl> : Invalid token")
                    return False   
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <func_decl> : Invalid token")
                return False 
        else:
            if DEBUG:
                print("Error in Parser: Non-terminal: <func_decl> : Invalid token")
            return False                                        


    def func_decl_new(self):
        if DEBUG:
            print("<func_decl_new> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] == '(':
            self.scanner.get_next_token()
            if self.parameter_list():
                if self.scanner.get_next_token()['value'] == ')':
                    if DEBUG:
                        print("<func_decl_new> : return True")
                    return True
                else:
                    if DEBUG:
                        print("Error in Parser: Non-terminal: <func_decl_new> : Invalid token")
                    return False 
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <func_decl_new> : Error from <parameter_list>")
                return False                                    
        else:
            if DEBUG:
                print("Error in Parser: Non-terminal: <func_decl_new> : Invalid token")
            return False             


    def type_name(self):
        if DEBUG:
            print("<type_name> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] in ['int', 'void', 'binary', 'decimal']:
            self.scanner.get_next_token()
            return True
        else:
            if DEBUG:
                print("Error in Parser: Non-terminal: <type_name> : Invalid token")
            return False 
     
    def parameter_list(self):
        if DEBUG:
            print("<parameter_list> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] == 'void':
            self.scanner.get_next_token()
            if self.parameter_list_z():
                if DEBUG:
                    print("<parameter_list> : return True")
                return True
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <parameter_list> : Error from <non_empty_list_prime>")
                return False
        elif lookahead['value'] == 'int':
            self.scanner.get_next_token()
            if self.scanner.get_next_token()['type'] == TOKEN_TYPES.IDENTIFIER:
                if self.non_empty_list_prime():
                    if DEBUG:
                        print("<parameter_list> : return True")
                    return True
                else:
                    if DEBUG:
                        print("Error in Parser: Non-terminal: <parameter_list> : Error from <non_empty_list_prime>")
                    return False
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <parameter_list> : Error from <non_empty_list_prime>")
                return False               
        elif lookahead['value'] == 'binary':
            self.scanner.get_next_token()
            if self.scanner.get_next_token()['type'] == TOKEN_TYPES.IDENTIFIER:
                if self.non_empty_list_prime():
                    if DEBUG:
                        print("<parameter_list> : return True")
                    return True
                else:
                    if DEBUG:
                        print("Error in Parser: Non-terminal: <parameter_list> : Error from <non_empty_list_prime>")
                    return False
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <parameter_list> : Error from <non_empty_list_prime>")
                return False 
        elif lookahead['value'] == 'decimal':
            self.scanner.get_next_token()
            if self.scanner.get_next_token()['type'] == TOKEN_TYPES.IDENTIFIER:
                if self.non_empty_list_prime():
                    if DEBUG:
                        print("<parameter_list> : return True")
                    return True
                else:
                    if DEBUG:
                        print("Error in Parser: Non-terminal: <parameter_list> : Error from <non_empty_list_prime>")
                    return False
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <parameter_list> : Error from <non_empty_list_prime>")
                return False 
        else:
            if DEBUG:
                print("<parameter_list> : return True")
            return True   



    def parameter_list_z(self):
        if DEBUG:
            print("<parameter_list_z> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['type'] == TOKEN_TYPES.IDENTIFIER:
            self.scanner.get_next_token()
            if self.non_empty_list_prime():
                if DEBUG:
                    print("<parameter_list_z> : return True")
                return True
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <parameter_list_z> : Error from <non_empty_list_prime>")
                return False   
        else:
            if DEBUG:
                print("<parameter_list_z> : return True")
            return True  

    def non_empty_list(self):
        if DEBUG:
            print("<non_empty_list> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] in ['int', 'void', 'binary', 'void']:
            self.scanner.get_next_token()
            if self.scanner.get_next_token()['type'] == TOKEN_TYPES.IDENTIFIER:
                if self.non_empty_list_prime():
                    if DEBUG:
                        print("<non_empty_list> : return True")
                    return True
                else:
                    if DEBUG:
                        print("Error in Parser: Non-terminal: <non_empty_list> : Error from <non_empty_list_prime>")
                    return False 
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <non_empty_list> : Invalid token")
                return False  
        else:
            if DEBUG:
                print("Error in Parser: Non-terminal: <non_empty_list> : Invalid token")
            return False   

    def non_empty_list_prime(self):
        if DEBUG:
            print("<non_empty_list_prime> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] == ',':
            self.scanner.get_next_token()
            if self.scanner.get_next_token()['type'] ==  TOKEN_TYPES.IDENTIFIER:
                if self.non_empty_list_prime():
                    if DEBUG:
                        print("<non_empty_list_prime> : return True")
                    return True
                else:
                    if DEBUG:
                        print("Error in Parser: Non-terminal: <non_empty_list_prime> : Error from <non_empty_list_prime>")
                    return False 
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <non_empty_list_prime> : Invalid token")
                return False                                                               
        else:
            if DEBUG:
                print("<non_empty_list_prime> : return True")
            return True   


    def data_decls(self):
        if DEBUG:
            print("<data_decls> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] in ['int', 'void', 'binary', 'void']:
            self.scanner.get_next_token()
            if self.id_list():
                if self.scanner.get_next_token()['value'] == ';':
                    self.variable_count = self.variable_count + 1
                    #self.scanner.get_next_token()
                    if self.data_decls():
                        if DEBUG:
                            print("<data_decls> : return True")
                        return True
                    else:
                        if DEBUG:
                            print("Error in Parser: Non-terminal: <data_decls> : Error from <data_decls>")
                        return False                        
                else:
                    if DEBUG:
                        print("Error in Parser: Non-terminal: <data_decls> : Invalid token")
                    return False 
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <data_decls> : Error from <id_list>")
                return False                                                               
        else:
            if DEBUG:
                print("<data_decls> : return True")
            return True 


    def data_decls_new(self):
        if DEBUG:
            print("<data_decls_new> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] in ['[', ';', ','] :
            if self.id_z():
                if self.id_list_prime():
                    if self.scanner.get_next_token()['value'] == ';':
                        self.variable_count = self.variable_count + 1
                        if self.data_or_func_decl():
                            if DEBUG:
                                print("<data_decls_new> : return True")
                            return True
                        else:
                            if DEBUG:
                                print("Error in Parser: Non-terminal: <data_decls_new> : Error from <data_or_func_decl>")
                            return False                            
                    else: 
                        if DEBUG:
                            print("Error in Parser: Non-terminal: <data_decls_new> : Invalid token")
                        return False        
                else:
                    if DEBUG:
                        print("Error in Parser: Non-terminal: <data_decls_new> : Error from <id_list_prime>")
                    return False                     
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <data_decls_new> : Error from <id_z>")
                return False  
        else:
            if DEBUG:
                print("Error in Parser: Non-terminal: <data_decls_new> : Invalid token")
            return False           

    def data_or_func_decl(self):
        if DEBUG:
            print("<data_or_func_decl> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] in ['int', 'void', 'binary', 'void']:
            self.scanner.get_next_token()
            if self.scanner.get_next_token()['type'] == TOKEN_TYPES.IDENTIFIER:
                if self.data_or_func_decl_z():
                    if DEBUG:
                        print("<data_or_func_decl> : return True")
                    return True
                else:
                    if DEBUG:
                        print("Error in Parser: Non-terminal: <data_or_func_decl> : Error from <data_or_func_z>")
                    return False  
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <data_or_func_decl> : Invalid token")
                return False 
        else:
            if DEBUG:
                print("<data_or_func_decl> : return True")
            return True


    def data_or_func_decl_z(self):
        if DEBUG:
            print("<data_or_func_decl_z> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] in ['[', ';', ',']:
            if self.data_decls_new():
                if DEBUG:
                    print("<data_or_func_decl_z> : return True")
                return True
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <data_or_func_decl_z> : Error from <data_decls_new>")
                return False                
        elif lookahead['value'] == '(':
            if self.func_list_new():
                if DEBUG:
                    print("<data_or_func_decl_z> : return True")
                return True
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <data_or_func_decl_z> : Error from <func_list_new>")
                return False 
        else:
            if DEBUG:
                print("Error in Parser: Non-terminal: <data_or_func_decl_z> : Invalid Token")
            return False            



    def id_list(self):
        if DEBUG:
            print("<id_list> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['type'] ==  TOKEN_TYPES.IDENTIFIER:
            if self.id():
                if self.id_list_prime():
                    if DEBUG:
                        print("<id_list> : return True")
                    return True
                else:
                    if DEBUG:
                        print("Error in Parser: Non-terminal: <id_list> : Error from <id_list_prime>")
                    return False 
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <id_list> : Error from <id>")
                return False
        else:
            if DEBUG:
                print("Error in Parser: Non-terminal: <id_list> : Invalid Token")
            return False                           
                                       

    def id_list_prime(self):
        if DEBUG:
            print("<id_list_prime> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] == ',':
            self.variable_count = self.variable_count + 1
            self.scanner.get_next_token()
            if self.id():
                if DEBUG:
                    print("<id_list_prime> : return True")
                return True
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <id_list_prime> : Error from <id_list_prime>")
                return False 
        else:
            if DEBUG:
                print("<id_list_prime> : return True")
            return True               

    def id(self):
        if DEBUG:
            print("<id> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['type'] == TOKEN_TYPES.IDENTIFIER:
            self.scanner.get_next_token()
            if self.id_z():       
                if DEBUG:
                    print("<id> : return True")
                return True
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <id> : Error from <id_z>")
                return False      
        else:
            if DEBUG:
                print("Error in Parser: Non-terminal: <id> : Invalid Token")
            return False                        


    def id_z(self):
        if DEBUG:
            print("<id_z> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] == '[':
            self.scanner.get_next_token()
            if self.expression():
                if self.scanner.get_next_token()['value'] == ']': 
                    if DEBUG:
                        print("<id_z> : return True")
                    return True
                else:
                    if DEBUG:
                        print("Error in Parser: Non-terminal: <id_z> : Invalid Token")
                    return False                           
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <id_z> : Error from <expression>")
                return False      
        else:
            if DEBUG:
                print("<id_z> : return True")
            return True


    def block_statements(self):
        if DEBUG:
            print("<block_statements> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] == '{':
            self.scanner.get_next_token()
            if self.statements():
                if DEBUG:
                    print("matching closing brace")
                if self.scanner.get_next_token()['value'] == '}':
                    if DEBUG:
                        print("<block_statements> : return True")
                    return True
                else:
                    if DEBUG:
                        print("Error in Parser: Non-terminal: <block_statements> : Invalid Token")
                    return False        
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <block_statements> : Error from <statements>")
                return False                             
        else:
            if DEBUG:
                print("Error in Parser: Non-terminal: <block_statements> : Invalid Token")
            return False    

    def statements(self):
        if DEBUG:
            print("<statements> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)  
        if lookahead['type']  == TOKEN_TYPES.IDENTIFIER or  lookahead['value'] in ['if', 'while', 'return', 'break', 'continue', 'read', 'write', 'print']:
            if self.statement():
                if self.statements():
                    if DEBUG:
                        print("<statements> : return True")     
                    return True
                else:
                    if DEBUG:
                        print("Error in Parser: Non-terminal: <statements> : Error from <statements>")
                    return False                 
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <statements> : Error from <statement>")
                return False  
        else:
            if DEBUG:
                print("<statements> : return True")  
            return True                

    def statement(self):
        if DEBUG:
            print("<statement> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1) 
        if lookahead['type']  == TOKEN_TYPES.IDENTIFIER:
            self.scanner.get_next_token()
            if self.statement_z():
                self.statement_count = self.statement_count + 1
                if DEBUG:
                    print("<statement> : return True")
                return True
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <statement> : Error from <statement_z>")
                return False                 
        elif lookahead['value']  == 'if':
            if self.if_statement():
                self.statement_count = self.statement_count + 1
                if DEBUG:
                    print("<statement> : return True")
                return True
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <statement> : Error from <if_statement>")
                return False
        elif lookahead['value']  == 'while':
            if self.while_statement():
                self.statement_count = self.statement_count + 1
                if DEBUG:
                    print("<statement> : return True")
                return True
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <statement> : Error from <while_statement>")
                return False
        elif lookahead['value']  == 'return':
            if self.return_statement():
                self.statement_count = self.statement_count + 1
                if DEBUG:
                    print("<statement> : return True")
                return True
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <statement> : Error from <return_statement>")
                return False
        elif lookahead['value']  == 'break':
            if self.break_statement():
                self.statement_count = self.statement_count + 1
                if DEBUG:
                    print("<statement> : return True")
                return True
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <statement> : Error from <break_statement>")
                return False
        elif lookahead['value']  == 'continue':
            if self.continue_statement():
                self.statement_count = self.statement_count + 1
                if DEBUG:
                    print("<statement> : return True")
                return True
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <statement> : Error from <continue_statement>")
                return False
        elif lookahead['value']  == 'read':
            self.scanner.get_next_token()
            if self.scanner.get_next_token()['value'] == '(':
                if self.scanner.get_next_token()['type'] == TOKEN_TYPES.IDENTIFIER:
                    if self.scanner.get_next_token()['value'] == ')':
                        if self.scanner.get_next_token()['value'] == ';':
                            self.statement_count = self.statement_count + 1
                            if DEBUG:
                                print("<statement> : return True")
                            return True
                        else:
                            if DEBUG:
                                print("Error in Parser: Non-terminal: <statement> : Invalid Token")
                            return False
                    else:
                        if DEBUG:
                            print("Error in Parser: Non-terminal: <statement> : Invalid Token")
                        return False                        
                else:
                    if DEBUG:
                        print("Error in Parser: Non-terminal: <statement> : Invalid Token")
                    return False 
            else:
                if DEBUG:               
                    print("Error in Parser: Non-terminal: <statement> : Invalid Token")
                return False                           
        elif lookahead['value']  == 'write':
            self.scanner.get_next_token()
            if self.scanner.get_next_token()['value'] == '(':
                if self.expression():
                    if self.scanner.get_next_token()['value'] == ')':
                        if self.scanner.get_next_token()['value'] == ';':
                            self.statement_count = self.statement_count + 1
                            if DEBUG:
                                print("<statement> : return True")
                            return True
                        else:
                            if DEBUG:
                                print("Error in Parser: Non-terminal: <statement> : Invalid Token")
                            return False
                    else:
                        if DEBUG:
                            print("Error in Parser: Non-terminal: <statement> : Invalid Token")
                        return False   
                else:
                    if DEBUG:
                        print("Error in Parser: Non-terminal: <statement> : Error from <expression>")
                    return False   
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <statement> : Invalid Token")
                return False   
        elif lookahead['value']  == 'print':
            self.scanner.get_next_token()
            if self.scanner.get_next_token()['value'] == '(':
                if self.scanner.get_next_token()['type'] == TOKEN_TYPES.STRING:
                    if self.scanner.get_next_token()['value'] == ')':
                        if self.scanner.get_next_token()['value'] == ';':
                            self.statement_count = self.statement_count + 1
                            if DEBUG:
                                print("<statement> : return True")
                            return True
                        else:
                            if DEBUG:
                                print("Error in Parser: Non-terminal: <statement> : Invalid Token")
                            return False                            
                    else:
                        if DEBUG:
                            print("Error in Parser: Non-terminal: <statement> : Invalid Token")
                        return False  
                else:
                    if DEBUG:
                        print("Error in Parser: Non-terminal: <statement> : Invalid Token")
                    return False 
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <statement> : Invalid Token")
                return False   
        else:
            if DEBUG:
                print("Error in Parser: Non-terminal: <statement> : Invalid Token")
            return False            



    def statement_z(self):
        if DEBUG:
            print("<statement_z> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] in ['[', '=']:
            if self.id_z():
                if self.scanner.get_next_token()['value'] == '=':
                    if self.expression():
                        if self.scanner.get_next_token()['value'] == ';':
                            if DEBUG:
                                print("<statement_z> : return True")
                            return True
                        else:
                            if DEBUG:
                                print("Error in Parser: Non-terminal: <statement_z> : Invalid Token")
                            return False                            
                    else:
                        if DEBUG:
                            print("Error in Parser: Non-terminal: <statement_z> : Error from <expression>")
                        return False                        

                else:
                    if DEBUG:
                        print("Error in Parser: Non-terminal: <statement_z> : Invalid Token")
                    return False 
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <statement_z> : Error from <id_z>")
                return False          
        elif lookahead['value'] == '(':
            self.scanner.get_next_token()
            if self.expr_list():
                if self.scanner.get_next_token()['value'] == ')':
                    if self.scanner.get_next_token()['value'] == ';':
                        if DEBUG:
                            print("<statement_z> : return True")
                        return True
                    else:
                        if DEBUG:
                            print("Error in Parser: Non-terminal: <statement_z> : Invalid Token")
                        return False                       
                else:
                    if DEBUG:
                        print("Error in Parser: Non-terminal: <statement_z> : Invalid Token")
                    return False                    
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <statement_z> : Error from <expr_list>")
                return False 
        else:
            if DEBUG:
                print("Error in Parser: Non-terminal: <statement_z> : Invalid Token")
            return False 



    def assignment(self):
        if DEBUG:
            print("<assignment> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['type'] == TOKEN_TYPES.IDENTIFIER:
            if self.id():
                if self.scanner.get_next_token()['value'] == '=':
                    if self.expression():
                        if self.scanner.get_next_token()['value'] == ';':
                            if DEBUG:
                                print("<assignment> : return True")
                            return True
                        else:
                            if DEBUG:
                                print("Error in Parser: Non-terminal: <assignment> : Invalid Token")
                            return False  
                    else:
                        if DEBUG:
                            print("Error in Parser: Non-terminal: <assignment> : Error from <expression>")
                        return False                                                  
                else:
                    if DEBUG:
                        print("Error in Parser: Non-terminal: <assignment> : Invalid Token")
                    return False 
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <assignment> : Error from <id>")
                return False                
        else:
            if DEBUG:
                print("Error in Parser: Non-terminal: <assignment> : Invalid Token")
            return False 
    


    def func_call(self):
        if DEBUG:
            print("<func_call> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)                   
        if  lookahead['type'] == TOKEN_TYPES.IDENTIFIER:
            self.scanner.get_next_token()
            if self.scanner.get_next_token()['value'] == '(':
                if self.expr_list():
                    if self.scanner.get_next_token()['value'] == ')':
                        if self.scanner.get_next_token()['value'] == ';':
                            if DEBUG:
                                print("<func_call> : return True")
                            return True
                        else:
                            if DEBUG:
                                print("Error in Parser: Non-terminal: <func_call> : Invalid Token")
                            return False                            
                    else:
                        if DEBUG:
                            print("Error in Parser: Non-terminal: <func_call> : Invalid Token")
                        return False                        
                else:
                    if DEBUG:
                        print("Error in Parser: Non-terminal: <func_call> : Error from <expr_list>")
                    return False  
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <func_call> : Invalid Token")
                return False                  
        else:
            if DEBUG:
                print("Error in Parser: Non-terminal: <func_call> : Invalid Token")
            return False  



    def expr_list(self):
        if DEBUG:
            print("<expr_list> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)   
        if lookahead['type'] == TOKEN_TYPES.IDENTIFIER or lookahead['type'] == TOKEN_TYPES.NUMBER or  lookahead['value'] in ['-', '(']:
            if self.non_empty_expr_list():
                if DEBUG:
                    print("<expr_list> : return True")
                return True
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <expr_list> : Error from <non_empty_expr_list>")
                return False                
        else:
            if DEBUG:
                print("<expr_list> : return True")
            return True            



    def non_empty_expr_list(self):
        if DEBUG:
            print("<non_empty_expr_list> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)   
        if lookahead['type'] == TOKEN_TYPES.IDENTIFIER or lookahead['type'] == TOKEN_TYPES.NUMBER or  lookahead['value'] in ['-', '(']:
            if self.expression():
                if self.non_empty_expr_list_prime():
                    if DEBUG:
                        print("<non_empty_expr_list> : return True")
                    return True
                else:
                    if DEBUG:
                        print("Error in Parser: Non-terminal: <non_empty_expr_list> : Error from <non_empty_expr_list_prime>")
                    return False
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <non_empty_expr_list> : Error from <expression>")
                return False                               
        else:
            if DEBUG:
                print("Error in Parser: Non-terminal: <non_empty_expr_list> : Invalid Token")
            return False               



    def non_empty_expr_list_prime(self):
        if DEBUG:
            print("<non_empty_expr_list_prime> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] == ',':
            self.scanner.get_next_token()
            if self.expression():
                if self.non_empty_expr_list_prime():
                    if DEBUG:
                        print("<non_empty_expr_list_prime> : return True")
                    return True
                else:
                    if DEBUG:
                        print("Error in Parser: Non-terminal: <non_empty_expr_list> : Error from <expression>")
                    return False                     
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <non_empty_expr_list> : Error from <expression>")
                return False                  
        else:
            if DEBUG:
                print("<non_empty_expr_list_prime> : return True")
            return True 



    def if_statement(self):
        if DEBUG:
            print("<if_statement> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] == 'if':
            self.scanner.get_next_token()
            if self.scanner.get_next_token()['value'] == '(':
                if self.condition_expression():
                    if self.scanner.get_next_token()['value'] == ')':
                        if self.block_statements():
                            if DEBUG:
                                print("<if_statement> : return True")
                            return True
                        else:
                            if DEBUG:
                                print("Error in Parser: Non-terminal: <if_statement> : Error from <block_statements>")
                            return False                            
                    else:
                        if DEBUG:
                            print("Error in Parser: Non-terminal: <if_statement> : Invalid Token")
                        return False                          
                else:
                    if DEBUG:
                        print("Error in Parser: Non-terminal: <if_statement> : Error from <condition_expression>")
                    return False   
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <if_statement> : Invalid Token")
                return False   
        else:
            if DEBUG:
                print("Error in Parser: Non-terminal: <if_statement> : Invalid Token")
            return False   



    def condition_expression(self):
        if DEBUG:
            print("<condition_expression> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['type'] == TOKEN_TYPES.IDENTIFIER or lookahead['type'] == TOKEN_TYPES.NUMBER or  lookahead['value'] in ['-', '(']: 
            if self.condition():
                if self.condition_expression_z():
                    if DEBUG:
                        print("<condition_expression> : return True")
                    return True
                else:
                    if DEBUG:
                        print("Error in Parser: Non-terminal: <condition_expression> : Error from <condition_expression_z>")
                    return False                 
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <condition_expression> : Error from <condition>")
                return False            
        else:
            if DEBUG:
                print("Error in Parser: Non-terminal: <condition_expression> : Invalid Token")
            return False     



    def  condition_expression_z(self):
        if DEBUG:
            print("<condition_expression_z> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] in ['&&', '||']:
            if self.condition_op():
                if self.condition():
                    if DEBUG:
                        print("<condition_expression_z> : return True")
                    return True
                else:
                    if DEBUG:
                        print("Error in Parser: Non-terminal: <condition_expression_z> : Error from <condition>")
                    return False                     
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <condition_expression_z> : Error from <condition_op>")
                return False  
        else:
            if DEBUG:
                print("<condition_expression_z> : return True")
            return True



    def  condition_op(self):
        if DEBUG:
            print("<condition_op> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] == '&&':
            self.scanner.get_next_token()
            if DEBUG:
                print("<condition_op> : return True")
            return True
        if lookahead['value'] == '||':
            self.scanner.get_next_token()
            if DEBUG:
                print("<condition_op> : return True")
            return True
        else:
            if DEBUG:
                print("Error in Parser: Non-terminal: <condition_op> : Invalid Token")
            return False            



    def condition(self):
        if DEBUG:
            print("<condition> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['type'] == TOKEN_TYPES.IDENTIFIER or lookahead['type'] ==  TOKEN_TYPES.NUMBER  or lookahead['value'] in ['-', '(']:
            if self.expression():
                if self.comparison_op():
                    if self.expression():
                        if DEBUG:
                            print("<condition> : return True")
                        return True
                    else:
                        if DEBUG:
                           print("Error in Parser: Non-terminal: <condition> : Error from <expression>")
                        return False   
                else:
                    if DEBUG:
                        print("Error in Parser: Non-terminal: <condition> : Error from <condition_op>")
                    return False                      
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <condition> : Error from <expression>")
                return False   
        else:
            if DEBUG:
                print("Error in Parser: Non-terminal: <condition> : Invalid Token")
            return False   



    def comparison_op(self):
        if DEBUG:
            print("<comparison_op> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] in ['==', '!=', '>', '>=', '<', '<=']:
            self.scanner.get_next_token()
            if DEBUG:
                print("<comparison_op> : return True")
            return True
        else:
            if DEBUG:
                print("Error in Parser: Non-terminal: <comparison_op> : Invalid Token")
            return False



    def while_statement(self):
        if DEBUG:
            print("<while_statement> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] == 'while':
            self.scanner.get_next_token()
            if self.scanner.get_next_token()['value'] == '(':
                if self.condition_expression():
                    if self.scanner.get_next_token()['value'] == ')':
                        if self.block_statements():
                            if DEBUG:
                                print("<while_statement> : return True")
                            return True
                        else:
                            if DEBUG:
                                print("Error in Parser: Non-terminal: <while_statement> : Error from <block_statements>")
                            return False                             
                    else:
                        if DEBUG:
                            print("Error in Parser: Non-terminal: <while_statement> : Invalid Token")
                        return False 
                else:
                    if DEBUG:
                        print("Error in Parser: Non-terminal: <while_statement> : Error from <condition_expression>")
                    return False 
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <while_statement> : Invalid Token")
                return False 
        else:
            if DEBUG:
                print("Error in Parser: Non-terminal: <while_statement> : Invalid Token")
            return False 


    def return_statement(self):
        if DEBUG:
            print("<return_statement> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] == 'return':
            self.scanner.get_next_token()
            if self.return_statement_z():
                if DEBUG:
                    print("<return_statement> : return True")
                return True
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <return_statement> : Error from <return_statement_z>")
                return False
        else:
            if DEBUG:
                print("Error in Parser: Non-terminal: <return_statement> : Invalid Token")
            return False                



    def return_statement_z(self):
        if DEBUG:
            print("<return_statement_z> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['type'] == TOKEN_TYPES.IDENTIFIER or lookahead['type'] ==  TOKEN_TYPES.NUMBER  or lookahead['value'] in ['-', '(']:
            if self.expression():
                if self.scanner.get_next_token()['value'] == ';':
                    if DEBUG:
                        print("<return_statement_z> : return True")
                    return True
                else:
                    if DEBUG:
                        print("Error in Parser: Non-terminal: <return_statement_z> : Invalid Token")
                    return False                   
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <return_statement_z> : Error from <expression>")
                return False
        elif lookahead['value'] == ';':
            self.scanner.get_next_token()
            if DEBUG:
                print("<return_statement_z> : return True")
            return True
        else:
            if DEBUG:
                print("Error in Parser: Non-terminal: <return_statement_z> : Invalid Token")
            return False                
        


    def break_statement(self):
        if DEBUG:
            print("<break_statement> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] == 'break':
            self.scanner.get_next_token()
            if self.scanner.get_next_token()['value'] == ';':
                if DEBUG:
                    print("<break_statement> : return True")
                return True
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <break_statement> : Invalid Token")
                return False               
        else:
            if DEBUG:
                print("Error in Parser: Non-terminal: <break_statement> : Invalid Token")
            return False



    def continue_statement(self):
        if DEBUG:
            print("<continue_statement> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] == 'continue':
            self.scanner.get_next_token()
            if self.scanner.get_next_token()['value'] ==  ';':
                if DEBUG:
                    print("<continue_statement> : return True")
                return True
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <continue_statement> : Invalid Token")
                return False     
        else:
            if DEBUG:
                print("Error in Parser: Non-terminal: <continue_statement> : Invalid Token")
            return False 



    def expression(self):
        if DEBUG:
            print("<expression> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['type'] == TOKEN_TYPES.IDENTIFIER or lookahead['type'] == TOKEN_TYPES.NUMBER or lookahead['value'] in ['-', '(']:
            if self.term():
                if self.expression_prime():
                    if DEBUG:
                        print("<expression> : return True")
                    return True
                else:
                    if DEBUG:
                        print("Error in Parser: Non-terminal: <expression> : Error from <expression_prime>")
                    return False  
            else:  
                if DEBUG:
                    print("Error in Parser: Non-terminal: <expression> : Error from <term>")
                return False  
        else:
            if DEBUG:
                print("Error in Parser: Non-terminal: <expression> : Invalid Token")
            return False  



    def expression_prime(self):
        if DEBUG:
            print("<expression_prime> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] in ['-', '+']:
            if self.addop():
                if self.term():
                    if self.expression_prime():
                        if DEBUG:
                            print("<expression_prime> : return True")
                        return True
                    else:
                        if DEBUG:
                            print("Error in Parser: Non-terminal: <expression_prime> : Error from <expression_prime>")
                        return False  
                else:
                    if DEBUG:
                        print("Error in Parser: Non-terminal: <expression_prime> : Error from <term>")
                    return False 
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <expression_prime> : Error from <addop>")
                return False 
        else:
            if DEBUG:
                print("<expression_prime> : return True")
            return True



    def addop(self):
        if DEBUG:
            print("<addop> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] in ['+', '-']:
            self.scanner.get_next_token()
            if DEBUG:
                print("<addop> : return True")
            return True
        else:
            if DEBUG:
                print("Error in Parser: Non-terminal: <addop> : Invalid Token")
            return False                 



    def term(self):
        if DEBUG:
            print("<term> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['type'] == TOKEN_TYPES.IDENTIFIER or lookahead['type'] == TOKEN_TYPES.NUMBER or lookahead['value'] in ['-', '(']:
            if self.factor():
                if self.term_prime():
                    if DEBUG:
                        print("<term> : return True")
                    return True
                else:
                    if DEBUG:
                        print("Error in Parser: Non-terminal: <term> : Invalid Token")
                    return False  
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <term> : Invalid Token")
                return False  
        else:
            if DEBUG:
                print("Error in Parser: Non-terminal: <term> : Invalid Token")
            return False  



    def term_prime(self):
        if DEBUG:
            print("<term_prime> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] in ['*', '/']:
            if self.mulop():
                if self.factor():
                    if self.term_prime():
                        if DEBUG:
                            print("<term_prime> : return True")
                        return True
                    else:
                        if DEBUG:
                            print("Error in Parser: Non-terminal: <term_prime> : Error from <term_prime>")
                        return False  
                else:
                    if DEBUG:
                        print("Error in Parser: Non-terminal: <term_prime> : Error from <factor>")
                    return False  
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <term_prime> : Error from <mulop>")
                return False      
        else:
            if DEBUG:
                print("<term_prime> : return True")
            return True 



    def mulop(self):
        if DEBUG:
            print("<mulop> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] in ['*', '/']:
            self.scanner.get_next_token()
            if DEBUG:
                print("<mulop> : return True")
            return True
        else:
            if DEBUG:
                print("Error in Parser: Non-terminal: <mulop> : Invalid Token")
            return False 



    def factor(self):
        if DEBUG:
            print("<factor> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['type'] == TOKEN_TYPES.IDENTIFIER:
            self.scanner.get_next_token()
            if self.factor_z():
                if DEBUG:
                    print("<factor> : return True")
                return True
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <factor> : Error from <factor_z>")
                return False                   
        elif lookahead['type'] == TOKEN_TYPES.NUMBER:
            self.scanner.get_next_token()
            if DEBUG:
                print("<factor> : return True")
            return True
        elif lookahead['value'] == '-':
            self.scanner.get_next_token()
            if self.scanner.get_next_token()['type'] == TOKEN_TYPES.NUMBER:
                if DEBUG:
                    print("<factor> : return True")
                return True
        elif lookahead['value'] == '(':
            self.scanner.get_next_token()
            if self.expression():
                if DEBUG:
                    print("after expression in <factor> : <%s> " % (self.scanner.token_lookahead(1)))
                if self.scanner.get_next_token()['value'] == ')':
                    if DEBUG:
                        print("<factor> : return True")
                    return True
                else:
                    if DEBUG:
                        print("Error in Parser: Non-terminal: <factor> : Invalid Token")
                    return False  
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <factor> : Error from <expression>")
                return False                                         
        else:
            if DEBUG:
                print("Error in Parser: Non-terminal: <factor> : Invalid Token")
            return False 



    def factor_z(self):
        if DEBUG:
            print("<factor_z> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] == '[':
            self.scanner.get_next_token()
            if self.expression():
                if self.scanner.get_next_token()['value'] == ']':
                    if DEBUG:
                        print("<factor_z> : return True")
                    return True
                else:
                    if DEBUG:
                        print("Error in Parser: Non-terminal: <factor_z> : Invalid Token")
                    return False                    
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <factor_z> : Error from <expression>")
                return False 
        elif lookahead['value'] == '(':
            self.scanner.get_next_token()
            if self.expr_list():
                if self.scanner.get_next_token()['value'] == ')':
                    if DEBUG:
                        print("<factor_z> : return True")
                    return True
                else:
                    if DEBUG:
                        print("Error in Parser: Non-terminal: <factor_z> : Invalid Token")
                    return False                           
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <factor_z> : Error from <expr_list>")
                return False   
        else:
            if DEBUG:
                print("<factor_z> : return True")
            return True

if __name__ == '__main__':
    if len(sys.argv) != 2:
       sys.exit()
    filename = sys.argv[1]
    parser = Parser(filename)
    if parser.program():
        print('pass variable %s function %s statement %s' % (parser.variable_count, parser.function_count, parser.statement_count))
    else:
        print('fail')


