
#!/usr/bin/python
"""
scanner.py (c) 2016 gmeneze@ncsu.edu, MIT licence
Part of project for course CSC 512: Compiler Construction
http://people.engr.ncsu.edu/xshen5/csc512_fall2016/projects/Scanner.html
USAGE: 
	python scanner.py <input_file>
OUTPUT:
	generates an output file with name obtained by appending "_gen" to the input file.
	This generated file should contain code which produces the same output as the original input file when compiled and executed.
"""

from __future__ import division,print_function
import sys,re,traceback,random, operator, string, time
sys.dont_write_bytecode=True

def enum(**enums):
    """ creates a mock enum type in python """
    return type('Enum', (), enums)

TOKEN_TYPES = enum(IDENTIFIER=1, NUMBER=2, RESERVED_WORD=3, SYMBOL=4, STRING=5, META_STATEMENT=6)

class Token(object):
    """ class to encapsulate all functionality related to tokens """
    reserved_words = ['int', 'void', 'if', 'while', 'return', 'read', 'write', 'print', 'continue', 'break', 'binary', 'decimal']
    symbols = ['(', ')', '{', '}', '[', ']', ',', ';', '+', '-', '*', '/', '==', '!=', '>', '>=', '<', '<=', '=', '&&', '||']

    @staticmethod
    def is_identifier(str, scanner):
    	""" identify if the input string is an identifier. 
    		Returns dictionary containing type and value if yes, else returns None. """
        if str[0].isalpha():
            for c in str[1:]:
                if not (c.isdigit() or c.isalpha() or c == "_"):
                    return None
            return {'type':TOKEN_TYPES.IDENTIFIER, 'value':str}
        else:
            return None

    @staticmethod
    def is_number(str, scanner):
        """ identify if the input string is a number. 
        	Returns dictionary containing type and value if yes, else returns None. """
        for c in str:
            if not (c.isdigit()):
                return None
        return {'type':TOKEN_TYPES.NUMBER, 'value':str}

    @staticmethod
    def is_reserved_word(str, scanner):
        """ identify if the input string is a reserved word. 
            Returns dictionary containing type and value if yes, else returns None. """
        if str in Token.reserved_words:
            return {'type':TOKEN_TYPES.RESERVED_WORD, 'value':str}
        else:
            return None

    @staticmethod
    def is_symbol(sym, scanner):
        """ identify if the input string is a symbol. 
            Returns dictionary containing type and value if yes, else returns None. """
        new_sym = sym + scanner.read(1)
        if new_sym in Token.symbols:
            return {'type':TOKEN_TYPES.SYMBOL, 'value':new_sym}
        else:
            scanner.consume(-1)
            if sym in Token.symbols:
                return {'type':TOKEN_TYPES.SYMBOL, 'value':sym}
            else:
                return None

    @staticmethod
    def is_string(str, scanner):
        """ identify if the input string is a string. 
            Returns dictionary containing type and value if yes, else returns None. """
        if len(str) > 1 and str[0] == '"' and str[-1] == '"':
            return {'type':TOKEN_TYPES.STRING, 'value':str}	
        elif str[0] == '"':
            char = scanner.read(1)
            while char != '"':
                if char == '':
                    raise ValueError('the input program is illegal')
                str = ''.join((str, char))
                char = scanner.read(1)
            return {'type':TOKEN_TYPES.STRING, 'value':str + char}  
        else:
			return None

    @staticmethod
    def is_meta_statement(str, scanner):
        """ identify if the input string is a meta statement. 
            Returns dictionary containing type and value if yes, else returns None. """
        if str[0] == '#':	
            char = scanner.read(1)
            while char not in ['\n','']:
                str = ''.join((str, char))
                char = scanner.read(1)
            return {'type':TOKEN_TYPES.META_STATEMENT, 'value':str}
        elif str[0] == '/':	
            char = scanner.read(1)
            if char == "/":
                while char not in ['\n','']:
                    str = ''.join((str, char))
                    char = scanner.read(1)
                return {'type':TOKEN_TYPES.META_STATEMENT, 'value':str}	
            else:
                scanner.consume(-1)		
                return None
        else:
            return None

    @staticmethod
    def classify(word, scanner):
        """ Identify the type of input word. 
            Returns dictionary containing type and value if identified, else returns None. """
#        print("input word is: <%s>" % (word))  // debug
        methods = [Token.is_reserved_word, Token.is_identifier, Token.is_number, Token.is_string, Token.is_meta_statement, Token.is_symbol]
        for method in methods:
            result = method(word, scanner)
            if result != None:
#                print("result is: <%s>" % (result)) // debug
                return result
#        print("result is: <%s>" % (result))  // debug
        return None

class Scanner(object):
    """ Encapsulate all functionality related to reading a file. """
    def __init__(self, filename):
        self.file = open(filename)

    def character(self):
        """ read input file one character at a time and yield.
            Provides an iterator over characters of the input file. """
        while True:
            char = self.read(1)
            if char == '':
                break
            yield char

    def word(self):
        """ read input file one word at a time. A word is a group of characters which are terminated
            by space or tab or newline or any of the symbols listed in Token.symbols. Each of these 
            delimiters are also considered words. """
        str = ""
        for c in self.character():
            if c in [' ', '\t','\n'] + Token.symbols:
                if str != "":
                    self.consume(-1)
                    yield str
                    str = ""
                else:
                    yield "" + c
            else:
                str = ''.join((str, c))
        if str != "":
            yield str		

    def read(self, number):
        """ Read given number of characters from the file, if file has already been read then the tell count 
            does not increase. This increment in positioning is done by this routine as the users of this function
            rely on the tell count being incremented after each read. """
        char = self.file.read(number)
        if char == '':
            self.file.seek(self.file.tell() + 1)	
        return char

    def consume(self, number):
        """ Does a relative seek to the specified position in the file """
        self.file.seek(number,1)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit()
    filename = sys.argv[1]
    filename_arr = filename.split(".")	
    new_filename = filename_arr[0] + "_gen." + filename_arr[1]
    scanner = Scanner(filename)
    target = open(new_filename, 'w')
    target.truncate()

    for word in scanner.word():
        dict=Token.classify(word,scanner)
        if dict!=None:
            if dict['type'] == TOKEN_TYPES.IDENTIFIER and dict['value'] != 'main':
                target.write("csc512" + dict['value'])
            elif dict['type'] == TOKEN_TYPES.META_STATEMENT:
                target.write(dict['value'] + "\n")
            else:
                target.write(dict['value'])
        else:
            if word in [' ', '\t']:
                target.write(word)
            elif word == '\n':
                continue
            else:
                target.write("\n!!ERROR!!\nThe word: <" + word + "> could not be classified as a valid token \nthe input program is illegal\n") 
                raise ValueError("\n!!ERROR!!\nThe word: <" + word + "> could not be classified as a valid token \nthe input program is illegal\n")
