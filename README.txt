How to run scanner?
No compilation is needed. 
Run it as follows :-
python Scanner.py <input-file>


Where is output file created?
In the same folder, the naming convention mentioned in project is followed. 
That is, "foo.c" will become "foo_gen.c". 


Scanner Implementation :-
1. Data Structures:
    - An enumeration is maintained for token types. 

    - The class Token encapsulates all functionality related to tokens 
        - list of reserved words 
        - list of symbols 
        - methods to identify token types.  

    - The class Scanner encapsulates all functionality related to reading the input file.
        - Iterator over characters of input file.
        - Method to return next token (if any) from the input file.
        - Method to check if next token exists in input file.
        - Method to read a given number of characters from input file.
        - Method to move file pointer to desired position relative to current position.

2. Flow:
    - Check if the input file contains next token.
    - Fetch the next token. 
    - The returned tuple contains token type and its value.
    - If token type is -1, then the token is invalid (could not be identified) and an error is raised.
    - If token type is IDENTIFIER and value of token is not "main" then append "cs512" to token and write it to output file.
    - If token type is META STATEMENT prepend a "\n" to it, this is because every META-STATEMENT needs to written on a new line.
    - All other tokens are to be written as is. 

3. Please Note:
    - Every meta-statement is preceded and followed by a new-line character. So, even if there is a comment on the same line as code, it is printed on next line.
      example: 
                int x; // meta-statement
      
      output:
                int cs512x; 

                // meta-statement

    - String cannot contain new-lines.
      example: The following string is invalid
                " this is a 
                  meta-statement"
