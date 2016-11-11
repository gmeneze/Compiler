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
import Queue
import copy
#from Scanner import Scanner, Token, TOKEN_TYPES, DEBUG
import sys,re,traceback,random, operator, string, time
def enum(**enums):
    """ creates a mock enum type in python """
    return type('Enum', (), enums)

TOKEN_TYPES = enum(IDENTIFIER=1, NUMBER=2, RESERVED_WORD=3, SYMBOL=4, STRING=5, META_STATEMENT=6)

sys.dont_write_bytecode=True

Token_queue = Queue.Queue()
Func_decl_queue = Queue.Queue()
Local_dict = {}
Gocal_dict = {}
Parameter_queue = Queue.Queue()
Token_stack = []
Expression_queue = Queue.Queue()

class Code_Generator(object):
    """ Encapsulate all functionality related to reading a file. """
    def __init__(self, filename):
        filename_arr = filename.split(".")
        new_filename = filename_arr[0] + "_gen." + filename_arr[1]
        self.file = open(new_filename, 'w')
        self.file.truncate()
        self.expression_token_counter = 0

    def add_to_dict(self, token):
    	global Local_dict
    	if token['value'] not in Local_dict:
    		Local_dict.update({token['value'] : len(Local_dict)})

    def print_global(self):
    	var_size = len(Local_dict)
    	if var_size > 0:
    		self.file.write("int global[" + str(var_size) + "];")
    		for key in Local_dict:
    			Global_dict = copy.deepcopy(Local_dict)	
		Local_dict.clear()

    def print_function(self):  #complete this function
        self.file.write("\n")
    	var_size = len(Local_dict)
    	if var_size > 0:
    		self.file.write("int local[" + str(var_size) + "];")
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
            if temp_token['value'] in Local_dict:
                self.file.write("local[" + str(Local_dict[temp_token['value']]) + "]")
            else:
                self.file.write(temp_token['value'])
        self.file.write("\n")
        Local_dict.clear()

    def print_function_declaration(self):
        self.file.write("\n")
        while Func_decl_queue.qsize() > 0:
            temp_token = Func_decl_queue.get()
            self.file.write(temp_token['value'])
        #self.file.write("\n")

    def resolve_expression(self):

        Expression_list = []
        while Expression_queue.qsize() > 0:
            Expression_list.append(Expression_queue.get())

        while(len(Expression_list) > 1):
            start_index = -1
            end_index = -1
            i = 0
            for i in range(len(Expression_list)):
                if Expression_list[i]['value'] == '(' and i-1 >= 0 and Expression_list[i-1]['type'] == TOKEN_TYPES.IDENTIFIER:
                    start_index = i
            
            if start_index != -1:
                bracket_counter = 0
                for i in range(start_index+1, len(Expression_list)):
                    if Expression_list[i]['value'] == '(':
                        bracket_counter = bracket_counter + 1

                    if Expression_list[i]['value'] == ')':
                        if bracket_counter == 0:
                            end_index = i
                            break
                        else:
                            bracket_counter = bracket_counter-1
            if start_index != -1:
                start_index = start_index+1
                end_index = end_index-1
                temp_queue = Queue.Queue()
                for index in range(start_index, end_index+1):
                    temp_queue.put(Expression_list[index])
                del(Expression_list[start_index:end_index+1])
                parameter_token = self.resolve_single_expression(temp_queue)

                function_name_token = Expression_list[start_index-2]
                print("start index is: " + str(start_index))
                del(Expression_list[start_index-2:start_index+1])

                final_token = self.get_function_token(function_name_token, parameter_token)

                Expression_list.insert(start_index-2, final_token)
            else:
                start_index = 0
                end_index = len(Expression_list)-1

                temp_queue = Queue.Queue()
                for index in range(start_index, end_index+1):
                    temp_queue.put(Expression_list[index])

                print("start index is: " + str(start_index))
                del(Expression_list[start_index:end_index+1])

                final_token = self.resolve_single_expression(temp_queue)
                Expression_list.insert(start_index, final_token)

        while len(Token_stack) > 0:
            temp_token = Token_stack.pop()
            print("temp token before putting in queue is: " + temp_token['value'])
            Token_queue.put(temp_token)

        space_separator = {'type':'SEPARATORS', 'value': ' '}
        Token_queue.put(space_separator)
        Token_queue.put(Expression_list[0])
        #self.expression_token_counter = 0

    def resolve_single_expression(self, queue):
        values_stack = []
        operator_stack = []
        #print("Expression queue size: " + str(Expression_queue.qsize()) + " length of token stack is: " + str(len(Token_stack)))
        while queue.qsize() != 0:
            token = queue.get()
            print("expression token is: " + token['value'])
            if token['type'] == TOKEN_TYPES.IDENTIFIER or token['type'] == TOKEN_TYPES.NUMBER:
                values_stack.append(token)
            elif self.is_left_parenthesis(token):
                operator_stack.append(token)
            elif self.is_right_parenthesis(token):
                print("is right parenthesis: " + token['value'])
                while len(operator_stack) > 0 and not self.is_left_parenthesis(operator_stack[-1]):
                    operator = operator_stack.pop()
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
                    result = apply_operator(operator, value_1, value_2)
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
        #print("resolve expression completed")

    def is_left_parenthesis(self, token):
        return token['value'] == '('

    def is_right_parenthesis(self, token):
        return token['value'] == ')'

    def is_operator(self, token):
        if token['value'] in ['(', ')', '*', '/', '+', '-']:
            return True
        else:
            return False

    def has_precedence(self, token1, token2):
        if token1['value'] == '(' or token2['value'] == '(':
            return False
        elif token1['value'] in ['*', '/'] and token2['value'] in ['+', '-']:
            return False
        else:
            return True

    def get_function_token(self, function_name_token, parameter_token):
        var_name = str(self.expression_token_counter) + "num"
        print("var name is: " + var_name)
        temp_token = {'type':TOKEN_TYPES.IDENTIFIER, 'value':var_name}
        self.add_to_dict(temp_token)
        equal_operator = {'type':TOKEN_TYPES.SYMBOL, 'value': '='}
        space_separator = {'type':'SEPARATORS', 'value': ' '}
        newline_separator = {'type':'SEPARATORS', 'value': '\n'}
        semicolon_operator = {'type':TOKEN_TYPES.SYMBOL, 'value': ';'}
        left_parenthesis = {'type':TOKEN_TYPES.SYMBOL, 'value': '('}
        right_parenthesis = {'type':TOKEN_TYPES.SYMBOL, 'value': ')'}
        Token_queue.put(temp_token)
        Token_queue.put(space_separator)
        Token_queue.put(equal_operator)
        Token_queue.put(space_separator)      
        Token_queue.put(function_name_token)
        Token_queue.put(left_parenthesis)
        Token_queue.put(parameter_token)
        Token_queue.put(right_parenthesis)
        Token_queue.put(semicolon_operator)
        Token_queue.put(newline_separator)
        self.expression_token_counter = self.expression_token_counter + 1
        return temp_token

    def apply_operator(self, operator, token1, token2):
        print("Token queue size in apply_operator: " + str(Token_queue.qsize()))
        var_name = str(self.expression_token_counter) + "num"
        print("var name is: " + var_name)
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
        self.expression_token_counter = self.expression_token_counter + 1
        print("Token queue size after apply_operator: " + str(Token_queue.qsize()))
        return temp_token


