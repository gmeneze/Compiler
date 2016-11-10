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
Local_dict = {}
Gocal_dict = {}

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
    		self.file.write("int global[" + str(var_size) + "]")
    		for key in Local_dict:
    			Global_dict = copy.deepcopy(Local_dict)	
		Local_dict.clear()

    def print_function(self):  #complete this function
    	var_size = len(Local_dict)
    	if var_size > 0:
    		self.file.write("int local[" + str(var_size) + "]")
		for key in Local_dict:
			Global_dict = copy.deepcopy(Local_dict)	
		Local_dict.clear()

	def temp_text(self):
		print("hey there")
