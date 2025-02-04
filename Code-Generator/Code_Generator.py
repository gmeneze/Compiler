#!/usr/bin/python
"""
Code_Generator.py (c) 2016 gmeneze@ncsu.edu, MIT licence
Part of project for course CSC 512: Compiler Construction
http://people.engr.ncsu.edu/xshen5/csc512_fall2016/projects/IntraFuncGen.html
USAGE: 
    This file is used by Parser.py.
    To run Parser :-
    python Parser.py <input_file> 
OUTPUT:
    The parser produces an intermediate code which is consistent with the grammar specified in requirement doc.
OUTPUT file name:
    <input_file_name>_gen.c
OUTPUT file location:
    output file is created in the same location as input    
"""
import Queue
import copy
import sys,re,traceback,random, operator, string, time
def enum(**enums):
    """ creates a mock enum type in python """
    return type('Enum', (), enums)

TOKEN_TYPES = enum(IDENTIFIER=1, NUMBER=2, RESERVED_WORD=3, SYMBOL=4, STRING=5, META_STATEMENT=6)
DEBUG = False
sys.dont_write_bytecode=True

# Global data structures 
Token_queue = Queue.Queue() # Buffer to hold function data.
Func_decl_queue = Queue.Queue()  # Buffer to hold function declarations.
Local_dict = {}  # Dictionary mapping local variables to local array index positions
Local_array_offset_dict = {}  # Dictionary mapping local array name to it's offset in local array
Local_array_size_dict = {}  # Dictionary mapping local array name to it's size.
Global_array_offset_dict = {} # Dictionary mapping global array to it's offset in global array.
Global_array_size_dict = {} # Dictionary mapping global array name to it's size.
Global_dict = {} # Dictionary mapping global variables to global array index position
Parameter_queue = Queue.Queue() # Buffer to hold functions parameter list
Token_stack = [] # Stack used for expression evaluation
Expression_queue = Queue.Queue() # Buffer to hold all tokens of an expression

class Code_Generator(object):
    """ Encapsulate all functionality related to Intermediate Code Generation. """
    def __init__(self, filename):
        filename_arr = filename.split(".")
        new_filename = filename_arr[0] + "_gen." + filename_arr[1]
        self.file = open(new_filename, 'w')
        self.file.truncate()
        self.expression_token_counter = 0
        self.local_array_size = 0
        self.global_array_size = 0
        self.condition_queue = Queue.Queue()

    def print_meta_statement(self):
        """ Meta statements are to be copied to output, as is"""
        if DEBUG:
            print("print_metastatement called")
        while Token_queue.qsize() > 0:
            temp_token = Token_queue.get()
            self.file.write(temp_token['value'])

    def add_to_dict(self, token):
        """ Adds new variables to per function dictionary, dictionary maps variables to local array indices """
        if DEBUG:
            print("add_to_dict called")
    	global Local_dict
    	if token['value'] not in Local_dict:
            Local_dict.update({token['value'] : self.local_array_size})
            self.local_array_size = self.local_array_size + 1

    def add_array_to_dict(self, list):
        """ Adds new arrays to per function array dictionaries, dictionary maps array name to local array offset and also size of array"""
        if DEBUG:
            print("add_array_to_dict called")
        global Local_array_offset_dict, Local_array_size_dict
        Local_array_offset_dict.update({list[0]['value'] : str(self.local_array_size)})
        Local_array_size_dict.update({list[0]['value'] : list[1]['value']}) 
        self.local_array_size = self.local_array_size + int(list[1]['value'])


    def create_condition_stack(self):
        """ Creates condition stack needed for handling of cases where there is a condition-op within a if/while statement, local variables used for <condition> """ 
        global Token_queue
        equal_operator = {'type':TOKEN_TYPES.SYMBOL, 'value': '='}
        space_separator = {'type':'SEPARATORS', 'value': ' '}
        newline_separator = {'type':'SEPARATORS', 'value': '\n'}
        semicolon_operator = {'type':TOKEN_TYPES.SYMBOL, 'value': ';'} 
        if_token = {'type':TOKEN_TYPES.RESERVED_WORD, 'value':'if'}
        left_parenthesis = {'type':TOKEN_TYPES.SYMBOL, 'value':'('}
        var_name = str(self.expression_token_counter) + "num"
        self.expression_token_counter = self.expression_token_counter + 1
        if DEBUG:
            print("In create_condition_stack, var name is: " + var_name)
        temp_token = {'type':TOKEN_TYPES.IDENTIFIER, 'value':var_name}
        self.add_to_dict(temp_token)

        condition_op_token = Token_queue.queue[-1]
        del(Token_queue.queue[-1])
        temp_stack = []
        while Token_queue.queue[-1]['value'] != '(':
            temp_stack.append(Token_queue.queue[-1])
            del(Token_queue.queue[-1])

        temp_stack.append(equal_operator)
        temp_stack.append(space_separator)
        temp_stack.append(temp_token)

        while Token_queue.queue[-1]['value'] != 'if':
            del(Token_queue.queue[-1])
        del(Token_queue.queue[-1])

        while len(temp_stack) > 0:
            Token_queue.put(temp_stack.pop())

        Token_queue.put(semicolon_operator)
        Token_queue.put(newline_separator)

        self.condition_queue.put(if_token)
        self.condition_queue.put(left_parenthesis)
        self.condition_queue.put(temp_token)
        self.condition_queue.put(space_separator)
        self.condition_queue.put(condition_op_token)


    def resolve_condition_stack(self):
        """ Operates on the stack created in 'create_condition_stack' and correctly fills in the Token Queue after creation of local variables for <condition>"""
        global Token_queue
        equal_operator = {'type':TOKEN_TYPES.SYMBOL, 'value': '='}
        space_separator = {'type':'SEPARATORS', 'value': ' '}
        newline_separator = {'type':'SEPARATORS', 'value': '\n'}
        semicolon_operator = {'type':TOKEN_TYPES.SYMBOL, 'value': ';'} 
        if_token = {'type':TOKEN_TYPES.RESERVED_WORD, 'value':'if'}
        left_parenthesis = {'type':TOKEN_TYPES.SYMBOL, 'value':'('}
        var_name = str(self.expression_token_counter) + "num"
        self.expression_token_counter = self.expression_token_counter + 1
        if DEBUG:
            print("In resolve_condition_stack, var name is: " + var_name)
        temp_token = {'type':TOKEN_TYPES.IDENTIFIER, 'value':var_name}
        self.add_to_dict(temp_token)

        temp_stack = []
        while Token_queue.queue[-1]['value'] != '\n':
            temp_stack.append(Token_queue.queue[-1])
            del(Token_queue.queue[-1])

        temp_stack.append(equal_operator)
        temp_stack.append(space_separator)
        temp_stack.append(temp_token)

        while len(temp_stack) > 0:
            Token_queue.put(temp_stack.pop())

        Token_queue.put(semicolon_operator)
        Token_queue.put(newline_separator)

        self.condition_queue.put(space_separator)
        self.condition_queue.put(temp_token)

        while self.condition_queue.qsize() > 0:
            Token_queue.put(self.condition_queue.get())       

    def print_global(self):
        """ prints out global variables to output file """
        if DEBUG:
            print("print_global called")
        global Global_dict, Global_array_offset_dict, Global_array_size_dict
    	if self.local_array_size > 0:
            self.file.write("int global[" + str(self.local_array_size) + "];")
            Global_dict = copy.deepcopy(Local_dict)	
            Global_array_offset_dict = copy.deepcopy(Local_array_offset_dict)
            Global_array_size_dict = copy.deepcopy(Local_array_size_dict)
            self.global_array_size = self.local_array_size
        self.clear_local_data_structures()   

    def print_function(self): 
        """ prints out entire translated function to output file """
        if DEBUG:
            print("print function called")
            print("Global Dict contents are :, Global_dict size is: " + str(len(Global_dict)) + " Global_array_offset_dict size is: " + str(len(Global_array_offset_dict)) + " Global_array_size_dict: " + str(len(Global_array_size_dict)))
            for key in Global_dict:
                print("key is: " + str(key) + " value is: " + str(Global_dict[key]))
            for key in Global_array_offset_dict:
                print("key is: " + str(key) + " value is: " + str(Global_array_offset_dict[key]))
            for key in Global_array_size_dict:
                print("key is: " + str(key) + " value is: " + str(Global_array_size_dict[key]))   

        self.file.write("\n")
    	var_size = len(Local_dict)
    	if var_size > 0:
    		self.file.write("int local[" + str(self.local_array_size) + "];")
        while Parameter_queue.qsize() > 0:
            temp_token = Parameter_queue.get()
            self.file.write("\nlocal[" + str(Local_dict[temp_token['value']]) + "] = " + temp_token['value'] + ";")
        while Token_queue.qsize() > 0:
            temp_token = Token_queue.get()
            if temp_token['type'] == 'SEPARATORS':
                self.file.write(temp_token['value'])
                if Token_queue.qsize() > 0:
                    temp_token = Token_queue.get()
                else:
                    break                    
            while temp_token['type'] == 'SEPARATORS' and Token_queue.qsize() > 0:
                temp_token = Token_queue.get()  
            if temp_token['type'] == 'ARRAY_OFFSET':
                if temp_token['value'] in Local_array_offset_dict:
                    self.file.write(str(Local_array_offset_dict[temp_token['value']]))
                else:
                    self.file.write(str(Global_array_offset_dict[temp_token['value']]))
            elif temp_token['value'] in Local_array_offset_dict: # array variable name
                self.file.write("local")
            elif temp_token['value'] in Local_dict:
                self.file.write("local[" + str(Local_dict[temp_token['value']]) + "]")
            elif temp_token['value'] in Global_dict:
                self.file.write("global[" + str(Global_dict[temp_token['value']]) + "]")
            elif temp_token['value'] in Global_array_offset_dict:
                self.file.write("global")
            else:
                self.file.write(temp_token['value'])
        self.file.write("\n")
        self.clear_local_data_structures()

    def clear_local_data_structures(self):
        """ Clears local data structures for a function, needed after - print_global, print_function 
        and after function declarations when not followed by body""" 
        global Parameter_queue
        Local_dict.clear()
        Local_array_size_dict.clear()
        Local_array_offset_dict.clear()   
        while Parameter_queue.qsize() > 0:
            Parameter_queue.get()   
        self.local_array_size = 0  

    def print_function_declaration(self):
        """ Prints function declaration to output file """
        if DEBUG:
            print("In print_function_declaration")
        self.file.write("\n")
        while Func_decl_queue.qsize() > 0:
            temp_token = Func_decl_queue.get()
            self.file.write(temp_token['value'])     

    def resolve_expression(self):
        """ Resolves expressions such that the correct precedence order of operators is used - BODMAS, 
        also handles function calls and array references within an expression """
        if DEBUG:
            print("In resolve_expression")

        Expression_list = []
        while Expression_queue.qsize() > 0:
            Expression_list.append(Expression_queue.get())

        if DEBUG:
            print("In resolve expression, Token_queue contents are :")
            for i in range(len(Token_stack)):
                print(Token_stack[i])

        while(len(Expression_list) > 1):
            start_index = -1
            end_index = -1
            i = 0
            bracket_token = None
            for i in range(len(Expression_list)):
                if Expression_list[i]['value'] in ['(', '['] and i-1 >= 0 and Expression_list[i-1]['type'] == TOKEN_TYPES.IDENTIFIER:
                    bracket_token = Expression_list[i]
                    start_index = i           
            if start_index != -1:
                bracket_counter = 0
                for i in range(start_index+1, len(Expression_list)):
                    if Expression_list[i]['value'] in ['(', '[']:
                        bracket_counter = bracket_counter + 1

                    if Expression_list[i]['value'] in [')', ']']:
                        if bracket_counter == 0:
                            end_index = i
                            break
                        else:
                            bracket_counter = bracket_counter-1
            if start_index != -1:
                start_index = start_index+1
                end_index = end_index-1
                temp_token_list = []
                for index in range(start_index, end_index+1):
                    temp_token_list.append(Expression_list[index])
                del(Expression_list[start_index:end_index+1])
                #parameter_token = self.resolve_single_expression(temp_queue)
                function_name_token = Expression_list[start_index-2]
                if DEBUG:
                    print("start index is: " + str(start_index))
                del(Expression_list[start_index-2:start_index+1])
                final_token = self.get_function_token(function_name_token, bracket_token, temp_token_list)
                Expression_list.insert(start_index-2, final_token)
            else:
                start_index = 0
                end_index = len(Expression_list)-1
                if DEBUG:
                    print("=== before final call, Expression list is ==")
                    for temp_token in Expression_list:
                        print(temp_token['value'])
                    print("============================================")
                temp_queue = Queue.Queue()
                for index in range(start_index, end_index+1):
                    temp_queue.put(Expression_list[index])
                if DEBUG:
                    print("start index is: " + str(start_index))
                del(Expression_list[start_index:end_index+1])

                final_token = self.resolve_single_expression(temp_queue)
                Expression_list.insert(start_index, final_token)

        while len(Token_stack) > 0:
            temp_token = Token_stack.pop()
            if DEBUG:
                print("temp token before putting in queue is: " + temp_token['value'])
            Token_queue.put(temp_token)

        space_separator = {'type':'SEPARATORS', 'value': ' '}
        Token_queue.put(space_separator)
        Token_queue.put(Expression_list[0])
        #self.expression_token_counter = 0

    def resolve_single_expression(self, queue):
        """ Used to resolve a single expression such as one within a function call in the expression or within array square brackets """
        values_stack = []
        operator_stack = []
        while queue.qsize() != 0:
            token = queue.get()
            if DEBUG:
                print("expression token is: " + str(token['value']))
            if token['type'] == TOKEN_TYPES.IDENTIFIER or token['type'] == TOKEN_TYPES.NUMBER or token['type'] == 'ARRAY_OFFSET':
                values_stack.append(token)
            elif self.is_left_parenthesis(token):
                operator_stack.append(token)
            elif self.is_right_parenthesis(token):
                if DEBUG:
                    print("is right parenthesis: " + token['value'])
                while len(operator_stack) > 0 and not self.is_left_parenthesis(operator_stack[-1]):
                    operator = operator_stack.pop()
                    if DEBUG:
                        print("operator: " + operator['value'])
                    value_2 = values_stack.pop()
                    value_1 = values_stack.pop()
                    result = self.apply_operator(operator, value_1, value_2)
                    values_stack.append(result)
                operator_stack.pop()
            elif self.is_operator(token):
                while len(operator_stack) > 0 and self.has_precedence(token, operator_stack[-1]):
                    operator = operator_stack.pop()
                    value_2 = values_stack.pop()
                    value_1 = values_stack.pop()
                    result = self.apply_operator(operator, value_1, value_2)
                    values_stack.append(result)
                operator_stack.append(token)
            prev_token = token
        while len(operator_stack) > 0:
            operator = operator_stack.pop()
            value_2 = values_stack.pop()
            value_1 = values_stack.pop()
            result = self.apply_operator(operator, value_1, value_2)
            values_stack.append(result)            

        if len(values_stack) == 0:
            return {'type': 'DUMMY', 'value':''}
        else:
            final_value = values_stack.pop()
            return final_value

    def is_left_parenthesis(self, token):
        """ returns True if input token is a left parenthesis, used by resolve_single_expression """
        return token['value'] == '('

    def is_right_parenthesis(self, token):
        """ returns True if input token is a right parenthesis, used by resolve_single_expression """
        return token['value'] == ')'

    def is_operator(self, token):
        """ returns True if input token is an operator, used by resolve_single_expression """
        if token['value'] in ['(', ')', '*', '/', '+', '-']:
            return True
        else:
            return False

    def has_precedence(self, token1, token2):
        """ used to evaluate precedence, returns true if token2 has higher or equal precedence as compared to token1
        as per BODMAS, used by resolve_single_expression """
        if token1['value'] == '(' or token2['value'] == '(':
            return False
        elif token1['value'] in ['*', '/'] and token2['value'] in ['+', '-']:
            return False
        else:
            return True

    def get_function_token(self, function_name_token, bracket_token, temp_token_list):
        """ resolves input to create a single token for a function call or array reference within an expression """
        if DEBUG:
            print("========IN GET_FUNCTION_TOKEN ==========")
            for temp_token in temp_token_list:
                print(temp_token['value'])
            print("========================================")

        var_name = str(self.expression_token_counter) + "num"
        self.expression_token_counter = self.expression_token_counter + 1
        if DEBUG:
            print("var name is: " + var_name)
        temp_token = {'type':TOKEN_TYPES.IDENTIFIER, 'value':var_name}
        self.add_to_dict(temp_token)
        equal_operator = {'type':TOKEN_TYPES.SYMBOL, 'value': '='}
        space_separator = {'type':'SEPARATORS', 'value': ' '}
        newline_separator = {'type':'SEPARATORS', 'value': '\n'}
        semicolon_operator = {'type':TOKEN_TYPES.SYMBOL, 'value': ';'}
        left_bracket = bracket_token
        right_bracket = {'type':TOKEN_TYPES.SYMBOL, 'value': ')'}
        if bracket_token['value'] == '[':
            right_bracket = {'type':TOKEN_TYPES.SYMBOL, 'value': ']'}

        parameter_token_list = []
        temp_queue = Queue.Queue()
        for list_token in temp_token_list:
            if list_token['value'] == ',':
                parameter_token_list.append(self.resolve_single_expression(temp_queue))
                parameter_token_list.append(list_token)
                temp_queue = Queue.Queue()
            else:
                temp_queue.put(list_token)

        parameter_token_list.append(self.resolve_single_expression(temp_queue))

        Token_queue.put(temp_token)
        Token_queue.put(space_separator)
        Token_queue.put(equal_operator)
        Token_queue.put(space_separator)      
        Token_queue.put(function_name_token)
        Token_queue.put(left_bracket)

        for parameter_token in parameter_token_list:
            Token_queue.put(parameter_token)

        Token_queue.put(right_bracket)
        Token_queue.put(semicolon_operator)
        Token_queue.put(newline_separator)
        return temp_token

    def apply_operator(self, operator, token1, token2):
        """ applies the specified operator in the order token1 operator token2 and pushes to the print queue"""
        if DEBUG:
            print("Token queue size in apply_operator: " + str(Token_queue.qsize()))
        var_name = str(self.expression_token_counter) + "num"
        self.expression_token_counter = self.expression_token_counter + 1
        if DEBUG:
            print("In apply_operator var name is: " + var_name)
        temp_token = {'type':TOKEN_TYPES.IDENTIFIER, 'value':var_name}
        self.add_to_dict(temp_token)
        equal_operator = {'type':TOKEN_TYPES.SYMBOL, 'value': '='}
        space_separator = {'type':'SEPARATORS', 'value': ' '}
        newline_separator = {'type':'SEPARATORS', 'value': '\n'}
        semicolon_operator = {'type':TOKEN_TYPES.SYMBOL, 'value': ';'}
        Token_queue.put(temp_token)
        Token_queue.put(space_separator)
        Token_queue.put(equal_operator)
        Token_queue.put(space_separator)
        Token_queue.put(token1)
        Token_queue.put(space_separator)
        Token_queue.put(operator)
        Token_queue.put(space_separator)
        Token_queue.put(token2)
        Token_queue.put(semicolon_operator)
        Token_queue.put(newline_separator)
        if DEBUG:
            print("Token queue size after apply_operator: " + str(Token_queue.qsize()))
        return temp_token


