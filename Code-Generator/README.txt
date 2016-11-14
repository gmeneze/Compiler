I. How to compile and run:
==========================
The source consists of three python files named Scanner.py, Code_Generator.py and Parser.py. The Parser and Scanner are similar to those submitted previously. The parser works on the same grammar submitted in the Parser project submission. Minute modifications made to parser and scanner, the modifications mainly involve storing data in a print buffer which is ultimately used to create the output file. The file Code_Generator.py contains code to process data in this buffer to generate the correct output.

The parser is the same recursive descent parser I submitted for parser project previously, modified such that it produces the generated code - which is written in an output file one function at a time.

Since code is written in python, no compilation is needed.

To run, open terminal (or command line) and type the following: (the % is to denote the terminal, it is not an actual input)


% python Parser.py /path/to/input/file

The output file is created in the same directory as input file.

If the input file is a directory, or does not exist, or can not be read, the program will error out. Trying to run the program without an input file will also cause the program to fail.

The outcome is either success or fail from the parser. If the parser succeeds then there is no output printed and a file with suffix '_gen' is created with the generated code.

On failure, the parser prints 'error'. Scanner errors are printed and are prefixed by 'Error in Scanner' in the output, if any.

In case of errors the output file will contain only those functions which were successfully translated.

An example:

% python Parser.py foo.c

Upon success this will create a foo_gen.c with the generated code in the same directory as input file.
It will also printout the number of variables, functions and statements on the terminal (since the parser is same as for last project).

The source is written for python 2.7 and up. It has been tested on the provided VCL environment.

II. Program functionality and brief description:
===============================================
The new file Code_Generator.py specifies the functions and global data structure go get the generated code using the Parser and Scanner. The parser and scanner populate these data structures, the rest of the parser and scanner is same as it was from the parser project (additional comments have been put in places to increase readability).

Overview of data structures used :-
- Data Dictionaries 
    1. Maintained for global data declarations and local data declarations (within a function). 
    2. The local data dictionaries are cleared out after parsing each function.
    3. 6 dictionaries used in all :-
        1) To maintain mapping of local variables to local array
        2) To maintain mapping of global variables to global array
        3) To maintain mapping of local array name to it's size.
        4) To maintain mapping of local array name to it's offset position in local array.
        5) To maintain mapping of global array name to it's size.
        6) To maintain mapping of global array name to it's offset position in global array.
    4. Whenever an array is referenced in the program, the offset will be added to the index to get the right element in local/global array.

- Queues
   1. Used as buffers for processing data and for printing to file.
   2. 4 Queues used in all :-
       1) A buffer to hold function declaration only, it is filled up whenever a new function declaration is encountered and is written immediately after declaration to output file.
       2) A buffer to hold function parameters only, it is filled up whenever function parameters are encountered and is written immediately after all parameters have been specified.
       3) A buffer which contains data to be written to output file in the correct order, per function. This buffer includes most data, except for that explained below. This buffer is written out whenever a function body is completed.
       4) A buffer to hold an entire expression. The expression is then broken down and processed to satisfy the specified conditions.

- Stack :- 
   1. One stack is used during expression evaluation, this stack holds temporary data which is eventually moved to the buffer containing function body.
   2. One stack is used in Parser to keep track of goto labels of while loops for break and continue statements.

Expression evaluation :-
Expression evaluation is done using the standard stack method of evaluation. This takes care of precedence.

Program assumptions:
- The program will give error if break and continue statements are used outside a loop body, which is conforming to the gcc standard.
- No array can be used as a function parameter, which meets to rules set out in the original grammar for Parser.
