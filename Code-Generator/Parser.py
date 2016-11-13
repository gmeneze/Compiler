#!/usr/bin/python
"""
parser.py (c) 2016 gmeneze@ncsu.edu, MIT licence
Part of project for course CSC 512: Compiler Construction
http://people.engr.ncsu.edu/xshen5/csc512_fall2016/projects/Parser.html
USAGE: 
    python Parser.py <input_file>
OUTPUT:
    Produces an output in the format of :-
    pass <number of variables> <number of functions> <number of statements>
    OR
    error
"""
# Handling for brackets ([]) within expressions and otherwise
# Handling for function declarations - eg - int a();

from __future__ import division,print_function
import Queue
from Scanner import Scanner, Token, TOKEN_TYPES, DEBUG
from Code_Generator import Code_Generator, Token_queue, Local_dict, Func_decl_queue,Parameter_queue, Expression_queue, Token_stack
import sys,re,traceback,random, operator, string, time
sys.dont_write_bytecode=True

FIRST_TIME_IND = True
DEBUG = True
#DATA_DECLARATION = False

class Parser(object):
    def __init__(self, filename):
        self.scanner = Scanner(filename)
        self.variable_count = 0
        self.function_count = 0
        self.statement_count = 0
        self.code_generator = Code_Generator(filename)
        self.DATA_DECLARATION_IND = False
        self.expression_counter = 0
        self.array_tokens_list = []
        self.goto_counter = 0
        self.innermost_while_exit_token = None
        self.innermost_while_enter_token = None

    def program(self):
        """ <program> --> empty
                        | <type name> ID <program z> """

        if DEBUG: 
            print("<program> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        # '' is interpreted as eof 
        lookahead = self.scanner.token_lookahead(1)
        print("print_metastatement calling")
        if lookahead['value'] == '':
            return True
        elif lookahead['value'] in ['int', 'void', 'binary', 'decimal']:
            #print("can call now?")
            temp_token = self.scanner.get_next_token()
            if Token_queue.qsize() > 0:
                self.code_generator.print_meta_statement()
            Token_queue.put(temp_token)
            #print("Got int")
            temp_token = self.scanner.get_next_token()
            if temp_token['type'] == TOKEN_TYPES.IDENTIFIER:
                lookahead = self.scanner.token_lookahead(1)
                if lookahead['value'] == '[':
                    self.array_tokens_list.append(temp_token)
                else:
                    Token_queue.put(temp_token)
                if self.program_z():
                    # check if parsing has been completed
                    temp_token = self.scanner.get_next_token()
                    if temp_token['value'] == '': 
                        Token_queue.put(temp_token)
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
        """ <program z> --> <data decls new>
                           | <func list new> """

        if DEBUG:
            print("<program_z> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1) 
        if lookahead['value'] in ['[', ';',',']:
            # This is a data declaration, so put in dictionary
            while Token_queue.qsize() > 0:
                temp_token = Token_queue.get()
                if temp_token['type'] == TOKEN_TYPES.IDENTIFIER:
                    self.code_generator.add_to_dict(temp_token)

            if self.data_decls_new():
                if DEBUG:
                    print("<program_z> : return True")
                return True
            else:
                if DEBUG:
                    print("Error in Parser : Non-terminal: <program_z> : Error from <data_decls_new>")
                return False                 
        elif lookahead['value'] == '(':
            while Token_queue.qsize() > 0:
                temp_token = Token_queue.get()
                print("putting in: [" + temp_token['value'] + "]")
                Func_decl_queue.put(temp_token)

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
        """ <func list> --> empty 
                          | <func> <func list> """

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
        """ <func list new> -->  <func decl new> <func z> <func list> """

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
        """ <func> --> <func decl> <func z> """

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
        """<func z> --> semicolon
                      | left_brace <data decls> <statements> right_brace """

        if DEBUG:
            print("<func_z> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1) 
        if lookahead['value'] == ';':      
            Func_decl_queue.put(self.scanner.get_next_token())
            self.code_generator.print_function_declaration()
            if DEBUG:
                print("<func_z> : return True")
            return True
        elif lookahead['value'] == '{':
            Func_decl_queue.put(self.scanner.get_next_token())
            self.code_generator.print_function_declaration()
            #Token_queue.put(self.scanner.get_next_token())
            if self.data_decls():
                if DEBUG:
                    print("glen 1 <func_z> called with input : <%s> " % (self.scanner.token_lookahead(1)))
                if self.statements():
                    if DEBUG:
                        print("glen 2 <func_z> called with input : <%s> " % (self.scanner.token_lookahead(1)))
                    temp_token = self.scanner.get_next_token()
                    if temp_token['value'] == '}':
                        Token_queue.put(temp_token)
                        self.code_generator.print_function()
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
        """ <func decl> --> <type name> ID left_parenthesis <parameter list> right_parenthesis """

        if DEBUG:
            print("<func_decl> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] in ['int', 'void', 'binary', 'decimal']:
            Func_decl_queue.put(self.scanner.get_next_token())
            temp_token = self.scanner.get_next_token()
            if temp_token['type'] == TOKEN_TYPES.IDENTIFIER:
                Func_decl_queue.put(temp_token)
                temp_token = self.scanner.get_next_token()
                if temp_token['value'] == '(':
                    Func_decl_queue.put(temp_token)
                    if self.parameter_list():
                        temp_token = self.scanner.get_next_token()
                        if temp_token['value'] == ')':
                            Func_decl_queue.put(temp_token)
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
        """ <func decl new> --> left_parenthesis <parameter list> right_parenthesis """

        if DEBUG:
            print("<func_decl_new> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] == '(':
            Func_decl_queue.put(self.scanner.get_next_token())
            if self.parameter_list():
                temp_token = self.scanner.get_next_token()
                if temp_token['value'] == ')':
                    Func_decl_queue.put(temp_token)
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
        """ <type name> --> int 
                            | void 
                            | binary 
                            | decimal """

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
        """ <parameter list> --> empty 
                                | void <parameter list z>
                                | int ID <non-empty list prime> 
                                | binary ID <non-empty list prime> 
                                | decimal ID <non-empty list prime> """

        if DEBUG:
            print("<parameter_list> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] == 'void':
            Func_decl_queue.put(self.scanner.get_next_token())
            if self.parameter_list_z():
                if DEBUG:
                    print("<parameter_list> : return True")
                return True
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <parameter_list> : Error from <non_empty_list_prime>")
                return False
        elif lookahead['value'] == 'int':
            Func_decl_queue.put(self.scanner.get_next_token())
            temp_token = self.scanner.get_next_token()
            if temp_token['type'] == TOKEN_TYPES.IDENTIFIER:
                self.code_generator.add_to_dict(temp_token)
                Func_decl_queue.put(temp_token)
                Parameter_queue.put(temp_token)
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
            Func_decl_queue.put(self.scanner.get_next_token())
            temp_token = self.scanner.get_next_token()
            if temp_token['type'] == TOKEN_TYPES.IDENTIFIER:
                self.code_generator.add_to_dict(temp_token)
                Func_decl_queue.put(temp_token)
                Parameter_queue.put(temp_token)
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
            Func_decl_queue.put(self.scanner.get_next_token())
            temp_token = self.scanner.get_next_token()
            if temp_token['type'] == TOKEN_TYPES.IDENTIFIER:
                self.code_generator.add_to_dict(temp_token)
                Func_decl_queue.put(temp_token)
                Parameter_queue.put(temp_token)
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
        """ <parameter list z> --> empty
                     | ID <non-empty list prime> """
        if DEBUG:
            print("<parameter_list_z> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['type'] == TOKEN_TYPES.IDENTIFIER:
            temp_token = self.scanner.get_next_token()
            self.code_generator.add_to_dict(temp_token)
            Func_decl_queue.put(temp_token)
            Parameter_queue.put(temp_token)
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
        """ <non-empty list> --> <type name> ID <non-empty list prime> """

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
        """ <non-empty list prime> --> empty
                         | comma <type name> ID <non-empty list prime> """

        if DEBUG:
            print("<non_empty_list_prime> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] == ',':
            Func_decl_queue.put(self.scanner.get_next_token())
            temp_token = self.scanner.get_next_token()
            if temp_token['value'] in ['int', 'void', 'binary', 'decimal']:
                Func_decl_queue.put(temp_token)
                temp_token = self.scanner.get_next_token()
                if temp_token['type'] ==  TOKEN_TYPES.IDENTIFIER:
                    self.code_generator.add_to_dict(temp_token)
                    Func_decl_queue.put(temp_token)
                    Parameter_queue.put(temp_token)
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
                    print("Error in Parser: Non-terminal: <non_empty_list_prime> : Invalid token")
                return True    
        else:
            if DEBUG:
                print("<non_empty_list_prime> : return True")
            return True   


    def data_decls(self):
        """ <data decls> --> empty 
               | <type name> <id list> semicolon <data decls> """
        #global DATA_DECLARATION
        if DEBUG:
            print("<data_decls> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] in ['int', 'void', 'binary', 'decimal']:
            self.scanner.get_next_token()
            self.DATA_DECLARATION_IND  = True
            print("DATA_DECLARATION set to True "  + str(self.DATA_DECLARATION_IND))
            if self.id_list():
                if self.scanner.get_next_token()['value'] == ';':
                    self.DATA_DECLARATION_IND  = False
                    print("DATA_DECLARATION set to False "  + str(self.DATA_DECLARATION_IND ))
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
        """ <data decls new> --> <id z> <id list prime> semicolon <data or func decl> """

        if DEBUG:
            print("<data_decls_new> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] in ['[', ';', ','] :
            self.DATA_DECLARATION_IND  = True
            print("DATA_DECLARATION set to True "  + str(self.DATA_DECLARATION_IND ))
            if self.id_z():
                if self.id_list_prime():
                    if self.scanner.get_next_token()['value'] == ';':
                        self.DATA_DECLARATION_IND  = False
                        print("DATA_DECLARATION set to False "  + str(self.DATA_DECLARATION_IND ))
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
        """ <data or func decl> --> <type name> ID <data or func decl z> 
                                    | empty """
        if DEBUG:
            print("<data_or_func_decl> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] in ['int', 'void', 'binary', 'void']:
            Token_queue.put(self.scanner.get_next_token())
            temp_token = self.scanner.get_next_token()
            if temp_token['type'] == TOKEN_TYPES.IDENTIFIER:
                lookahead = self.scanner.token_lookahead(1)
                if lookahead['value'] == '[':
                    self.array_tokens_list.append(temp_token)
                else:
                    Token_queue.put(temp_token)
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
        """  <data or func decl z> --> <data decls new>
                                     | <func list new> """
        global FIRST_TIME_IND
        if DEBUG:
            print("<data_or_func_decl_z> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] in ['[', ';', ',']:
            while Token_queue.qsize() > 0:
                temp_token = Token_queue.get()
                if temp_token['type'] == TOKEN_TYPES.IDENTIFIER:
                    self.code_generator.add_to_dict(temp_token)
            if self.data_decls_new():
                if DEBUG:
                    print("<data_or_func_decl_z> : return True")
                return True
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <data_or_func_decl_z> : Error from <data_decls_new>")
                return False                
        elif lookahead['value'] == '(':
            while Token_queue.qsize() > 0:
                temp_token = Token_queue.get()
                print("putting in: [" + temp_token['value'] + "]")
                Func_decl_queue.put(temp_token)
            if FIRST_TIME_IND:
                self.code_generator.print_global()
                FIRST_TIME_IND = False
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
        """ <id list> --> <id> <id list prime> """

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
        """ <id list prime> --> empty
                              | comma <id> <id list prime> """

        if DEBUG:
            print("<id_list_prime> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] == ',':
            self.variable_count = self.variable_count + 1
            if not self.DATA_DECLARATION_IND:
                Token_queue.put(self.scanner.get_next_token())
            else:
                self.scanner.get_next_token()
            if self.id():
                if self.id_list_prime():
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
        """ <id> --> ID <id z> """

        if DEBUG:
            print("<id> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['type'] == TOKEN_TYPES.IDENTIFIER:
            temp_token = self.scanner.get_next_token()
            lookahead = self.scanner.token_lookahead(1)
            if lookahead['value'] == '[':
                self.array_tokens_list.append(temp_token)
            else:
                self.code_generator.add_to_dict(temp_token)
            if not self.DATA_DECLARATION_IND:  # Fix adding to dict
                #print("DATA_DECLARATION: " + str(self.DATA_DECLARATION_IND ) + " temp_token: " + temp_token['value']) 
                Token_queue.put(temp_token)
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


    def id_z(self):  #Handling not done
        """ <id z> --> empty
                    | left_bracket <expression> right_bracket """

        if DEBUG:
            print("<id_z> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] == '[':
            if self.DATA_DECLARATION_IND:
                self.scanner.get_next_token()
                temp_token = self.scanner.get_next_token()
                if temp_token['type'] == TOKEN_TYPES.NUMBER:
                    self.array_tokens_list.append(temp_token)           
                    if self.scanner.get_next_token()['value'] == ']': 
                        self.code_generator.add_array_to_dict(self.array_tokens_list)
                        self.array_tokens_list = []
                        if DEBUG:
                            print("<id_z> : return True")
                        return True
                    else:
                        if DEBUG:
                            print("Error in Parser: Non-terminal: <id_z> : Invalid Token")
                        return False                          
            else:
                temp_token = {'type':'ARRAY_OFFSET', 'value': Token_queue.queue[-1]['value']}
                addition_token = {'type':TOKEN_TYPES.SYMBOL, 'value': '+'}
                Token_queue.put(self.scanner.get_next_token())
                Expression_queue.put(temp_token)
                Expression_queue.put(addition_token)
                if self.expression():
                    print("After expression returns")
                    temp_token = self.scanner.get_next_token()
                    if temp_token['value'] == ']': 
                        #print("After expression returns")
                        Token_queue.put(temp_token)
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
        """ <block statements> --> left_brace <statements> right_brace """

        if DEBUG:
            print("<block_statements> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] == '{':
            self.scanner.get_next_token()
            if self.statements():
                if DEBUG:
                    print("matching closing brace")
                temp_token = self.scanner.get_next_token()
                if temp_token['value'] == '}':
                    #Token_queue.put(temp_token)
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
        """ <statements> --> empty 
                            | <statement> <statements> """

        if DEBUG:
            print("<statements> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)  
        if lookahead['type'] == TOKEN_TYPES.IDENTIFIER or lookahead['value'] in ['if', 'while', 'return', 'break', 'continue', 'read', 'write', 'print']:
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
        """ <statement> --> ID <statement z>
              | <if statement> 
              | <while statement> 
              | <return statement> 
              | <break statement> 
              | <continue statement> 
              | read left_parenthesis ID right_parenthesis semicolon 
              | write left_parenthesis <expression> right_parenthesis semicolon 
              | print left_parenthesis STRING right_parenthesis semicolon """

        if DEBUG:
            print("<statement> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1) 
        if lookahead['type']  == TOKEN_TYPES.IDENTIFIER:
            Token_queue.put(self.scanner.get_next_token())
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
            Token_queue.put(self.scanner.get_next_token())
            temp_token = self.scanner.get_next_token()
            if temp_token['value'] == '(':
                Token_queue.put(temp_token)
                temp_token = self.scanner.get_next_token()
                if temp_token['type'] == TOKEN_TYPES.IDENTIFIER:
                    Token_queue.put(temp_token)
                    temp_token = self.scanner.get_next_token()
                    if temp_token['value'] == ')':
                        Token_queue.put(temp_token)
                        temp_token = self.scanner.get_next_token()
                        if temp_token['value'] == ';':
                            Token_queue.put(temp_token)
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
            Token_queue.put(self.scanner.get_next_token())
            temp_token = self.scanner.get_next_token()
            if temp_token['value'] == '(':
                Token_queue.put(temp_token)
                if self.expression():
                    temp_token = self.scanner.get_next_token()
                    if temp_token['value'] == ')':
                        Token_queue.put(temp_token)
                        temp_token = self.scanner.get_next_token()
                        if temp_token['value'] == ';':
                            Token_queue.put(temp_token)
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
            Token_queue.put(self.scanner.get_next_token())
            temp_token = self.scanner.get_next_token()
            if temp_token['value'] == '(':
                Token_queue.put(temp_token)
                temp_token = self.scanner.get_next_token()
                if temp_token['type'] == TOKEN_TYPES.STRING:
                    Token_queue.put(temp_token)
                    temp_token = self.scanner.get_next_token()
                    if temp_token['value'] == ')':
                        Token_queue.put(temp_token)
                        temp_token = self.scanner.get_next_token()
                        if temp_token['value'] == ';':
                            Token_queue.put(temp_token)
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
        """ <statement z> --> <id z> equal_sign <expression> semicolon 
                            | left_parenthesis <expr list> right_parenthesis semicolon """

        if DEBUG:
            print("<statement_z> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] in ['[', '=']:
            if self.id_z():
                temp_token = self.scanner.get_next_token()
                if temp_token['value'] == '=':
                    Token_queue.put(temp_token)
                    if self.expression():
                        temp_token = self.scanner.get_next_token()
                        if temp_token['value'] == ';':
                            Token_queue.put(temp_token)
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
            Token_queue.put(self.scanner.get_next_token())
            if self.expr_list():
                temp_token = self.scanner.get_next_token()
                if temp_token['value'] == ')':
                    Token_queue.put(temp_token)
                    temp_token = self.scanner.get_next_token()
                    if temp_token['value'] == ';':
                        Token_queue.put(temp_token)
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
        """ <assignment> --> <id> equal_sign <expression> semicolon """

        if DEBUG:
            print("<assignment> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['type'] == TOKEN_TYPES.IDENTIFIER:
            if self.id():
                temp_token = self.scanner.get_next_token()
                if temp_token['value'] == '=':
                    Token_queue.put(temp_token)
                    if self.expression():
                        temp_token = self.scanner.get_next_token()
                        if temp_token['value'] == ';':
                            Token_queue.put(temp_token)
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
        """ <func call> --> ID left_parenthesis <expr list> right_parenthesis semicolon """

        if DEBUG:
            print("<func_call> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)                   
        if  lookahead['type'] == TOKEN_TYPES.IDENTIFIER:
            Token_queue.put(self.scanner.get_next_token())
            temp_token = self.scanner.get_next_token()
            if temp_token['value'] == '(':
                Token_queue.put(temp_token)
                if self.expr_list():
                    temp_token = self.scanner.get_next_token()
                    if temp_token['value'] == ')':
                        Token_queue.put(temp_token)
                        temp_token = self.scanner.get_next_token()
                        if temp_token['value'] == ';':
                            Token_queue.put(temp_token)
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
        """ <expr list> --> empty 
                            | <non-empty expr list> """

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
        """ <non-empty expr list> --> <expression> <non-empty expr list prime> """

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
        """ <non-empty expr list prime> --> empty
                              | comma <expression> <non-empty expr list prime> """

        if DEBUG:
            print("<non_empty_expr_list_prime> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] == ',':
            if Expression_queue.qsize() > 0:
                Expression_queue.put(self.scanner.get_next_token())
            else:
                Token_queue.put(self.scanner.get_next_token())
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
        """ <if statement> --> if left_parenthesis <condition expression> right_parenthesis <block statements> """

        if DEBUG:
            print("<if_statement> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] == 'if':
            Token_queue.put(self.scanner.get_next_token())
            temp_token = self.scanner.get_next_token()
            if temp_token['value'] == '(':
                Token_queue.put(temp_token)
                if self.condition_expression():
                    temp_token = self.scanner.get_next_token()
                    if temp_token['value'] == ')':
                        Token_queue.put(temp_token)
                        
                        goto_token_1 = {'type':TOKEN_TYPES.RESERVED_WORD, 'value': 'goto c' + str(self.goto_counter)}
                        target_token_1 = {'type':TOKEN_TYPES.RESERVED_WORD, 'value': 'c' + str(self.goto_counter) + ':'}
                        
                        self.goto_counter = self.goto_counter + 1
                        
                        semicolon_token = {'type':TOKEN_TYPES.SYMBOL, 'value': ';'}
                        newline_token =  {'type':TOKEN_TYPES.SYMBOL, 'value': '\n'}
                        
                        Token_queue.put(goto_token_1)
                        Token_queue.put(semicolon_token)
                        Token_queue.put(newline_token)
                        
                        goto_token_2 = {'type':TOKEN_TYPES.RESERVED_WORD, 'value': 'goto c' + str(self.goto_counter)}
                        target_token_2 = {'type':TOKEN_TYPES.RESERVED_WORD, 'value': 'c' + str(self.goto_counter) + ':'}
                        
                        self.goto_counter = self.goto_counter + 1
                        
                        Token_queue.put(goto_token_2)
                        Token_queue.put(semicolon_token)
                        Token_queue.put(newline_token)
                        
                        Token_queue.put(target_token_1)
                        Token_queue.put(semicolon_token)
                        Token_queue.put(newline_token)

                        if self.block_statements():
                            Token_queue.put(target_token_2)
                            Token_queue.put(semicolon_token)
                            Token_queue.put(newline_token)
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
        """ <condition expression> -->  <condition> <condition expression z> """

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
        """ <condition expression z> --> empty
                           | <condition op> <condition>  """

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
        """ <condition op> --> double_and_sign 
                 | double_or_sign """

        if DEBUG:
            print("<condition_op> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] == '&&':
            Token_queue.put(self.scanner.get_next_token())
            if DEBUG:
                print("<condition_op> : return True")
            return True
        if lookahead['value'] == '||':
            Token_queue.put(self.scanner.get_next_token())
            if DEBUG:
                print("<condition_op> : return True")
            return True
        else:
            if DEBUG:
                print("Error in Parser: Non-terminal: <condition_op> : Invalid Token")
            return False            



    def condition(self):
        """ <condition> --> <expression> <comparison op> <expression> """

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
        """ <comparison op> --> == 
                  | != 
                  | > 
                  | >= 
                  | < 
                  | <= """

        if DEBUG:
            print("<comparison_op> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] in ['==', '!=', '>', '>=', '<', '<=']:
            Token_queue.put(self.scanner.get_next_token())
            if DEBUG:
                print("<comparison_op> : return True")
            return True
        else:
            if DEBUG:
                print("Error in Parser: Non-terminal: <comparison_op> : Invalid Token")
            return False



    def while_statement(self):
        """ <while statement> --> while left_parenthesis <condition expression> right_parenthesis <block statements> """

        if DEBUG:
            print("<while_statement> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] == 'while':
            
            goto_token_0 = {'type':TOKEN_TYPES.RESERVED_WORD, 'value': 'goto c' + str(self.goto_counter)}
            target_token_0 = {'type':TOKEN_TYPES.RESERVED_WORD, 'value': 'c' + str(self.goto_counter) + ':'}  
            self.innermost_while_enter_token = goto_token_0

            semicolon_token = {'type':TOKEN_TYPES.SYMBOL, 'value': ';'}
            newline_token =  {'type':TOKEN_TYPES.SYMBOL, 'value': '\n'}

            self.goto_counter = self.goto_counter + 1       

            Token_queue.put(newline_token)
            Token_queue.put(target_token_0)
            Token_queue.put(semicolon_token)
            Token_queue.put(newline_token)
            
            if_token = {'type':TOKEN_TYPES.RESERVED_WORD, 'value': 'if'}
            self.scanner.get_next_token()
            Token_queue.put(if_token)
            temp_token = self.scanner.get_next_token()
            if temp_token['value'] == '(':
                Token_queue.put(temp_token)
                if self.condition_expression():
                    temp_token = self.scanner.get_next_token()
                    if temp_token['value'] == ')':
                        Token_queue.put(temp_token)
                        
                        goto_token_1 = {'type':TOKEN_TYPES.RESERVED_WORD, 'value': 'goto c' + str(self.goto_counter)}
                        target_token_1 = {'type':TOKEN_TYPES.RESERVED_WORD, 'value': 'c' + str(self.goto_counter) + ':'}
                        
                        self.goto_counter = self.goto_counter + 1
                        
                        Token_queue.put(goto_token_1)
                        Token_queue.put(semicolon_token)
                        Token_queue.put(newline_token)
                        
                        goto_token_2 = {'type':TOKEN_TYPES.RESERVED_WORD, 'value': 'goto c' + str(self.goto_counter)}
                        target_token_2 = {'type':TOKEN_TYPES.RESERVED_WORD, 'value': 'c' + str(self.goto_counter) + ':'}
                        self.innermost_while_exit_token = goto_token_2

                        self.goto_counter = self.goto_counter + 1
                        
                        Token_queue.put(goto_token_2)
                        Token_queue.put(semicolon_token)
                        Token_queue.put(newline_token)
                        
                        Token_queue.put(target_token_1)
                        Token_queue.put(semicolon_token)
                        Token_queue.put(newline_token)
                        if self.block_statements():

                            Token_queue.put(goto_token_0)
                            Token_queue.put(semicolon_token)
                            Token_queue.put(newline_token)

                            Token_queue.put(target_token_2)
                            Token_queue.put(semicolon_token)
                            Token_queue.put(newline_token)                            

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
        """ <return statement> --> return <return statement z> """

        if DEBUG:
            print("<return_statement> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] == 'return':
            Token_queue.put(self.scanner.get_next_token())
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
        """ <return statement z> --> <expression> semicolon 
                                    | semicolon """

        if DEBUG:
            print("<return_statement_z> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['type'] == TOKEN_TYPES.IDENTIFIER or lookahead['type'] ==  TOKEN_TYPES.NUMBER  or lookahead['value'] in ['-', '(']:
            if self.expression():
                temp_token = self.scanner.get_next_token()
                if temp_token['value'] == ';':
                    Token_queue.put(temp_token)
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
            Token_queue.put(self.scanner.get_next_token())
            if DEBUG:
                print("<return_statement_z> : return True")
            return True
        else:
            if DEBUG:
                print("Error in Parser: Non-terminal: <return_statement_z> : Invalid Token")
            return False                
        


    def break_statement(self):
        """ <break statement> ---> break semicolon """

        if DEBUG:
            print("<break_statement> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] == 'break':
            self.scanner.get_next_token()
            Token_queue.put(self.innermost_while_exit_token)
            temp_token = self.scanner.get_next_token()
            if temp_token['value'] == ';':
                Token_queue.put(temp_token)
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
        """ <continue statement> ---> continue semicolon """

        if DEBUG:
            print("<continue_statement> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] == 'continue':
            self.scanner.get_next_token()
            Token_queue.put(self.innermost_while_enter_token)
            temp_token = self.scanner.get_next_token()
            if temp_token['value'] ==  ';':
                Token_queue.put(temp_token)
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
        """ <expression> --> <term> <expression prime> """

        if DEBUG:
            print("<expression> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['type'] == TOKEN_TYPES.IDENTIFIER or lookahead['type'] == TOKEN_TYPES.NUMBER or lookahead['value'] in ['-', '(']:
            self.expression_counter = self.expression_counter + 1
            if Expression_queue.qsize() == 0 or (Expression_queue.qsize() == 2 and Expression_queue.queue[-2]['type'] == 'ARRAY_OFFSET'):
                while(Token_queue.qsize() > 0 and Token_queue.queue[-1]['value'] != '\n'):
                    Token_stack.append(Token_queue.queue[-1])
                    del(Token_queue.queue[-1])

            if self.term():
                if self.expression_prime():
                    self.expression_counter = self.expression_counter - 1
                    if self.expression_counter == 0:
                        self.code_generator.resolve_expression()
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
        """ <expression prime> --> empty
                     | <addop> <term> <expression prime> """

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
        """ <addop> --> plus_sign 
                     | minus_sign """

        if DEBUG:
            print("<addop> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] in ['+', '-']:
            Expression_queue.put(self.scanner.get_next_token())
            if DEBUG:
                print("<addop> : return True")
            return True
        else:
            if DEBUG:
                print("Error in Parser: Non-terminal: <addop> : Invalid Token")
            return False                 



    def term(self):
        """ <term> --> <factor> <term prime> """

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
        """ <term prime> --> empty
               | <mulop> <factor> <term prime> """

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
        """ <mulop> --> star_sign 
          | forward_slash """

        if DEBUG:
            print("<mulop> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] in ['*', '/']:
            Expression_queue.put(self.scanner.get_next_token())
            if DEBUG:
                print("<mulop> : return True")
            return True
        else:
            if DEBUG:
                print("Error in Parser: Non-terminal: <mulop> : Invalid Token")
            return False 



    def factor(self):
        """ <factor> --> ID <factor z>
           | NUMBER 
           | minus_sign NUMBER 
           | left_parenthesis <expression> right_parenthesis """

        if DEBUG:
            print("<factor> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['type'] == TOKEN_TYPES.IDENTIFIER:
            Expression_queue.put(self.scanner.get_next_token())
            if self.factor_z():
                if DEBUG:
                    print("<factor> : return True")
                return True
            else:
                if DEBUG:
                    print("Error in Parser: Non-terminal: <factor> : Error from <factor_z>")
                return False                   
        elif lookahead['type'] == TOKEN_TYPES.NUMBER:
            Expression_queue.put(self.scanner.get_next_token())
            if DEBUG:
                print("<factor> : return True")
            return True
        elif lookahead['value'] == '-':
            self.scanner.get_next_token()
            temp_token = self.scanner.get_next_token()
            if temp_token['type'] == TOKEN_TYPES.NUMBER:
                new_token = {'type' : temp_token['type'], 'value': '-' + temp_token['value']}
                Expression_queue.put(new_token)
                if DEBUG:
                    print("<factor> : return True")
                return True
        elif lookahead['value'] == '(':
            Expression_queue.put(self.scanner.get_next_token())
            if self.expression():
                if DEBUG:
                    print("after expression in <factor> : <%s> " % (self.scanner.token_lookahead(1)))
                temp_token = self.scanner.get_next_token()
                if temp_token['value'] == ')':
                    Expression_queue.put(temp_token)
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
        """ <factor z> --> empty
                        | left_bracket <expression> right_bracket 
                        | left_parenthesis <expr list> right_parenthesis """

        if DEBUG:
            print("<factor_z> called with input : <%s> " % (self.scanner.token_lookahead(1)))
        lookahead = self.scanner.token_lookahead(1)
        if lookahead['value'] == '[':
            temp_token = {'type':'ARRAY_OFFSET', 'value': Expression_queue.queue[-1]['value']}
            addition_token = {'type':TOKEN_TYPES.SYMBOL, 'value': '+'}
            Expression_queue.put(self.scanner.get_next_token())
            Expression_queue.put(temp_token)
            Expression_queue.put(addition_token)

            print("=====Expression queue in factor_z is:====")
            for i in range(Expression_queue.qsize()):
                print(Expression_queue.queue[i]['value'])
            print("=================================")
            if self.expression():
                temp_token = self.scanner.get_next_token()
                if temp_token['value'] == ']':
                    Expression_queue.put(temp_token)
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
            Expression_queue.put(self.scanner.get_next_token())
            if self.expr_list():
                temp_token = self.scanner.get_next_token()
                if temp_token['value'] == ')':
                    print("Expression_queue size: " + str(Expression_queue.qsize()))
                    Expression_queue.put(temp_token)
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
        print('error')


