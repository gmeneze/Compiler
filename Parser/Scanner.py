
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
    def is_identifier_or_reserved_word(character, scanner):
        """ identify if the input string is an identifier. 
            Returns dictionary containing type and value if yes, else returns None. """
        str = "" + character 
        for ch in scanner.character():
            if ch.isdigit() or ch.isalpha() or ch == "_":
                str = ''.join((str, ch))
            else:
                scanner.consume(-1)
                break

        if str in Token.reserved_words:
            return {'type':TOKEN_TYPES.RESERVED_WORD, 'value':str}
        else:
            return {'type':TOKEN_TYPES.IDENTIFIER, 'value':str}

    @staticmethod
    def is_number(character, scanner):
        """ identify if the input string is a number. 
            Returns dictionary containing type and value if yes, else returns None. """
        str = "" + character
        for ch in scanner.character():
            if ch.isdigit():
                str = ''.join((str, ch))
            else:
                scanner.consume(-1)
                break

        return {'type':TOKEN_TYPES.NUMBER, 'value':str}

    @staticmethod
    def is_symbol(character, scanner):
        """ identify if the input string is a symbol. 
            Returns dictionary containing type and value if yes, else returns None. """
        str = "" + character + scanner.read(1)
        if str in Token.symbols:
            return {'type':TOKEN_TYPES.SYMBOL, 'value':str}  
        elif character in Token.symbols:
            scanner.consume(-1)
            return {'type':TOKEN_TYPES.SYMBOL, 'value':character}
        else:
            scanner.consume(-1)
            return None

    @staticmethod
    def is_string(character, scanner):
        """ identify if the input string is a string. 
            Returns dictionary containing type and value if yes, else returns None. """
        str = "" + character
        for ch in scanner.character():
            str = ''.join((str, ch))    
            if ch == '\n':
                 raise ValueError("Multiline strings are not allowed")
            elif ch == '"':
                break

        if str[-1] != '"':
            raise ValueError("The string <" + "> was not terminated.")

        return {'type':TOKEN_TYPES.STRING, 'value':str}

    @staticmethod
    def is_meta_statement(character, scanner):
        """ identify if the input string is a meta statement. 
            Returns dictionary containing type and value if yes, else returns None. """
        if character == '/' and scanner.read(1) != '/':
            scanner.consume(-1)
            return Token.is_symbol(character, scanner)

        str = "" + character
        for ch in scanner.character():
            str = ''.join((str, ch))
            if ch == '\n':
                break    

        return {'type':TOKEN_TYPES.META_STATEMENT, 'value':str}

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

    def get_next_token(self):
        """ read input file one word at a time. A word is a group of characters which are terminated
            by space or tab or newline or any of the symbols listed in Token.symbols. Each of these 
            delimiters are also considered words. """
        for ch in self.character():
            if ch in [' ', '\n', '\t']:
                return {'type': 0, 'value':ch}  # 0 stands for delimiter
            elif ch.isalpha():
                return Token.is_identifier_or_reserved_word(ch, self)
            elif ch.isdigit():
                return Token.is_number(ch, self)
            elif ch == '"':
                return Token.is_string(ch, self)
            elif ch in ['#', '/']:
                return Token.is_meta_statement(ch, self)
            else:
                ret_val = Token.is_symbol(ch, self)
                if not ret_val:
                   return {'type': -1, 'value': ch}
                else:
                   return ret_val
        return  {'type': -1, 'value': ''}

    def token_lookahead(self, number):
        """ Used by LL(1) parser to look ahead by 1 """
        if self.has_more_tokens():
            return self.get_next_token()
        else:
            return {'type': -1, 'value': ''}


    def has_more_tokens(self):
        """ return True if there are more tokens which need to be processed. """
        ch = self.read(1)
        self.consume(-1)
        if ch == '':
            return False
        else:
            return True

    def read(self, number):
        """ Read given number of characters from the file, if file has already been read then the tell count 
            does not increase. This increment in positioning is done by this routine as the users of this function
            rely on the tell count being incremented after each read. """
        char = self.file.read(number)
        if char == '':
            self.file.seek(self.file.tell() + 1)    
        return char

    def consume(self, number):
        """ Does a relative seek to the specified position in the file. """
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

    while(scanner.has_more_tokens()):
        token = scanner.get_next_token()
        if  token['type'] == -1:
            target.write("\n!!ERROR!!\n <" + token['value'] + "> could not be classified as a valid token \nthe input program is illegal\n")
            raise ValueError("\n!!ERROR!!\n <" + token['value'] + "> could not be classified as a valid token \nthe input program is illegal\n") 
        elif token['type'] == TOKEN_TYPES.IDENTIFIER and token['value'] != 'main':
            target.write("cs512" + token['value'])
        elif token['type'] == TOKEN_TYPES.META_STATEMENT:
            target.write("\n" + token['value'])
        else:
            target.write(token['value'])
