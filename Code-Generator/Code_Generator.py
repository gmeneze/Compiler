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

Token_queue = Queue.Queue()
Local_dict = {}
Gocal_dict = {}

Class Code_Generator(object):
    """ Encapsulate all functionality related to reading a file. """
    def __init__(self, filename):
        filename_arr = filename.split(".")
        new_filename = filename_arr[0] + "_gen." + filename_arr[1]
        self.file = open(new_filename, 'w')
        self.file.truncate()

    def print_global(self):
    	var_size = Local_dict.qsize()
    	if(var_size > 0)
    		self.file.write("int global[" + var_size + "]")
    		for key in Local_dict:
    			Global_dict = copy.deepcopy(Local_dict)	
		Local_dict.clear()

	def print_code(self):
		while(Token_queue.qsize() > 0):
			token = Token_queue.get()	
			