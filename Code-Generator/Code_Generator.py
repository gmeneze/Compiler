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

import sys,re,traceback,random, operator, string, time
sys.dont_write_bytecode=True

Token_queue = Queue.Queue()
Func_decl_queue = Queue.Queue()
Local_dict = {}
Gocal_dict = {}
Parameter_queue = Queue.Queue()

class Code_Generator(object):
    """ Encapsulate all functionality related to reading a file. """
    def __init__(self, filename):
        filename_arr = filename.split(".")
        new_filename = filename_arr[0] + "_gen." + filename_arr[1]
        self.file = open(new_filename, 'w')
        self.file.truncate()

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
            self.file.write("\nlocal[" + str(Local_dict[temp_token['value']]) + "]=" + temp_token['value'] + ";")
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

    def print_function_declaration(self):
        self.file.write("\n")
        while Func_decl_queue.qsize() > 0:
            temp_token = Func_decl_queue.get()
            self.file.write(temp_token['value'])
        #self.file.write("\n")
