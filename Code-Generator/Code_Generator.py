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

Token_queue = Queue.Queue()
Local_dict = {}
Gocal_dict = {}

Class Code_Generator(object):
    def 