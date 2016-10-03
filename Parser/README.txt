A. Modified grammar used for the Parser:
=========================================

Following is the modified grammar used for the parser code submitted. This grammar is LL(1).

The following modification were done :-
 1. removal of all direct and indirect left recursion.
 2. left factoring and
 3. some substitution to reduce non-terminals. 

No. of rules in grammar: 96
No. of non-terminals in grammar: 49

Grammar:-
---------

 <program> --> empty
            | <type name> ID <program z> 

<program z> --> <data decls new>
              | <func list new>

<func list> --> empty 
              | <func> <func list> 

<func list new> -->  <func decl new> <func z> <func list> 

<func> --> <func decl> <func z> 

<func z> --> semicolon
           | left_brace <data decls> <statements> right_brace 

<func decl> --> <type name> ID left_parenthesis <parameter list> right_parenthesis 

<func decl new> --> left_parenthesis <parameter list> right_parenthesis

<type name> --> int 
              | void 
              | binary 
              | decimal 

<parameter list> --> empty 
                   | void <parameter list z>
                   | int ID <non-empty list prime> 
                   | binary ID <non-empty list prime> 
                   | decimal ID <non-empty list prime> 

<parameter list z> --> empty
                     | ID <non-empty list prime> 

<non-empty list> --> <type name> ID <non-empty list prime>

<non-empty list prime> --> empty
                         | comma <type name> ID <non-empty list prime>

<data decls> --> empty 
               | <type name> <id list> semicolon <data decls> 

<data decls new> --> <id z> <id list prime> semicolon <data or func decl>

<data or func decl> --> <type name> ID <data or func decl z> 
                      | empty

<data or func decl z> --> <data decls new>
                        | <func list new>

<id list> --> <id> <id list prime>

<id list prime> --> empty
                  | comma <id> <id list prime>

<id> --> ID <id z>

<id z> --> empty
         | left_bracket <expression> right_bracket

<block statements> --> left_brace <statements> right_brace 

<statements> --> empty 
               | <statement> <statements> 

<statement> --> ID <statement z>
              | <if statement> 
              | <while statement> 
              | <return statement> 
              | <break statement> 
              | <continue statement> 
              | read left_parenthesis ID right_parenthesis semicolon 
              | write left_parenthesis <expression> right_parenthesis semicolon 
              | print left_parenthesis STRING right_parenthesis semicolon 

<statement z> --> <id z> equal_sign <expression> semicolon 
                | left_parenthesis <expr list> right_parenthesis semicolon

<assignment> --> <id> equal_sign <expression> semicolon 

<func call> --> ID left_parenthesis <expr list> right_parenthesis semicolon 

<expr list> --> empty 
              | <non-empty expr list> 

<non-empty expr list> --> <expression> <non-empty expr list prime>

<non-empty expr list prime> --> empty
                              | comma <expression> <non-empty expr list prime>

<if statement> --> if left_parenthesis <condition expression> right_parenthesis <block statements> 

<condition expression> -->  <condition> <condition expression z>

<condition expression z> --> empty
                           | <condition op> <condition> 

<condition op> --> double_and_sign 
                 | double_or_sign 

<condition> --> <expression> <comparison op> <expression> 

<comparison op> --> == 
                  | != 
                  | > 
                  | >= 
                  | < 
                  | <=

<while statement> --> while left_parenthesis <condition expression> right_parenthesis <block statements> 

<return statement> --> return <return statement z>

<return statement z> --> <expression> semicolon
                       | semicolon 

<break statement> ---> break semicolon 

<continue statement> ---> continue semicolon

<expression> --> <term> <expression prime>

<expression prime> --> empty
                     | <addop> <term> <expression prime>

<addop> --> plus_sign 
          | minus_sign 

<term> --> <factor> <term prime>

<term prime> --> empty
               | <mulop> <factor> <term prime>

<mulop> --> star_sign 
          | forward_slash 

<factor> --> ID <factor z>
           | NUMBER 
           | minus_sign NUMBER 
           | left_parenthesis <expression> right_parenthesis

<factor z> --> empty
             | left_bracket <expression> right_bracket 
             | left_parenthesis <expr list> right_parenthesis 


FIRST and FOLLOW sets :-
-------------------------

1. <program>
    FIRST - {empty, int, void, binary, decimal}
    FOLLOW - {eof}

    FIRST+(<program> --> empty) --> {eof}
    FIRST+(<program> --> <type name> ID <program z>) --> {int, void, binary, decimal}


2. <program z>
    FIRST  - {left_bracket, semicolon, comma, left_parenthesis}
    FOLLOW - {eof}

    FIRST+(<program z> --> <data decls new>) --> {left_bracket, semicolon, comma}
    FIRST+(<program z> --> <func list new>) --> {left_parenthesis}


3. <func list>
    FIRST - {empty, int, void, binary, decimal}
    FOLLOW - {eof}

    FIRST+(<func list> --> empty) --> {eof} 
    FIRST+(<func list> --> <func> <func list>) --> {int, void, binary, decimal}


4. <func list new>
    FIRST - {left_parenthesis}
    FOLLOW - {eof}

    FIRST+(<func list new> -->  <func decl new> <func z> <func list>) --> {left_parenthesis}


5. <func>
    FIRST - {int, void, binary, decimal}
    FOLLOW - {int, void, binary, decimal, eof}

    FIRST+(<func> --> <func decl> <func z>) --> {int, void, binary, decimal}


6. <func z>
    FIRST - {semicolon, left_brace}
    FOLLOW - {int, void, binary, decimal, eof}

    FIRST+(<func z> --> semicolon) --> {semicolon}
    FIRST+(<func z> --> left_brace <data decls> <statements> right_brace) --> {left_brace}


7. <func decl>
    FIRST - {int, void, binary, decimal}
    FOLLOW - {semicolon, left_brace}

    FIRST+(<func decl> --> <type name> ID left_parenthesis <parameter list> right_parenthesis) --> {int, void, binary, decimal}


8. <func decl new>
    FIRST - {left_parenthesis}
    FOLLOW - {semicolon, left_brace}

    FIRST+(<func decl new> --> left_parenthesis <parameter list> right_parenthesis) --> {left_parenthesis}

9. <type name>
    FIRST - {int, void, binary, decimal}
    FOLLOW - {ID}

    FIRST+(<type name> --> int) --> {int}
    FIRST+(<type name> --> void) --> {void}
    FIRST+(<type name> --> binary) --> {binary}
    FIRST+(<type name> --> decimal) --> {decimal}


10. <parameter list>
    FIRST - {empty, int, void, binary, decimal}
    FOLLOW - {right_parenthesis}

    FIRST+(<parameter list> --> empty) --> {right_parenthesis}
    FIRST+(<parameter list> --> void <parameter list z>) --> {void}
    FIRST+(<parameter list> --> int ID <non-empty list prime>) --> {int}
    FIRST+(<parameter list> --> binary ID <non-empty list prime>)--> {binary}
    FIRST+(<parameter list> --> decimal ID <non-empty list prime>) --> {decimal}


11. <parameter list z>
    FIRST - {empty, ID}
    FOLLOW - {right_parenthesis}

    FIRST+(<parameter list z> --> empty) --> {right_parenthesis}
    FIRST+(<parameter list z> --> ID <non-empty list prime>) --> {ID}


12. <non-empty list>
    FIRST - {int, void, binary, decimal}
    FOLLOW - {}

    FIRST+(<non-empty list> --> <type name> ID <non-empty list prime>) --> {int, void, binary, decimal}

13. <non-empty list prime>
    FIRST - {empty, comma}
    FOLLOW - {right_parenthesis}

    FIRST+(<non-empty list prime> --> empty) --> {right_parenthesis}
    FIRST+(<non-empty list prime> --> comma <type name> ID <non-empty list prime>) --> {comma} 

14. <data decls>
    FIRST - {empty, int, void, binary, decimal}
    FOLLOW - {ID, if, while, return, break, continue, read, write, print, right_brace}

    FIRST+(<data decls> --> empty) -->  {ID, if, while, return, break, continue, read, write, print}
    FIRST+(<data decls> --> <type name> <id list> semicolon <data decls>) --> {int, void, binary, decimal}

15. <data decls new>
    FIRST - {left_bracket, semicolon, comma}
    FOLLOW - {eof}

    FIRST+(<data decls new> --> <id z> <id list prime> semicolon <data or func decl>) --> {left_bracket, semicolon, comma}


16. <data or func decl>
    FIRST - {empty, int, void, binary, decimal}
    FOLLOW - {eof}

    FIRST+(<data or func decl> --> <type name> ID <data or func decl z>) --> {int, void, binary, decimal}
    FIRST+(<data or func decl> --> empty) --> {eof}

17. <data or func decl z>
    FIRST - {left_bracket, semicolon, comma, left_parenthesis}
    FOLLOW - {eof}

    FIRST+(<data or func decl z> --> <data decls new>) --> {left_bracket, semicolon, comma}
    FIRST+(<data or func decl z> --> <func list new>) --> {left_parenthesis}

18. <id list>
    FIRST - {ID}
    FOLLOW - {semicolon}

    FIRST+(<id list> --> <id> <id list prime>) --> {ID}


19. <id list prime>
    FIRST - {empty, comma}
    FOLLOW - {semicolon}

    FIRST+(<id list prime> --> empty) --> {semicolon}
    FIRST+(<id list prime> --> comma <id> <id list prime>) --> {comma}


20. <id>
    FIRST - {ID}
    FOLLOW - {comma, semicolon, equal_sign}

    FIRST+(<id> --> ID <id z>) --> {ID}


21. <id z>
    FIRST - {empty, left_bracket}
    FOLLOW - {comma, semicolon, equal_sign}

    FIRST+(<id z> --> empty) --> {comma, semicolon, equal_sign}
    FIRST+(<id z> --> left_bracket <expression> right_bracket) --> {left_bracket}

22. <block statements>
    FIRST - {left_brace}
    FOLLOW - {right_brace}

    FIRST+(<block statements> --> left_brace <statements> right_brace) --> {left_brace}


23. <statements>
    FIRST - {empty, ID, if, while, return, break, continue, read, write, print}
    FOLLOW - {right_brace}

    FIRST+(<statements> --> empty) --> {right_brace}
    FIRST+(<statements> --> <statement> <statements>) --> {ID, if, while, return, break, continue, read, write, print}

24. <statement>
    FIRST - {ID, if, while, return, break, continue, read, write, print}
    FOLLOW - {right_brace, ID, if, while, return, break, continue, read, write, print}

    FIRST+(<statement> --> ID <statement z>) --> {ID}
    FIRST+(<statement> --> <if statement>) --> {if}
    FIRST+(<statement> --> <while statement>) --> {while}
    FIRST+(<statement> --> <return statement>) --> {return}
    FIRST+(<statement> --> <break statement>) --> {break}
    FIRST+(<statement> --> <continue statement>) --> {continue}
    FIRST+(<statement> --> read left_parenthesis ID right_parenthesis semicolon) --> {read}
    FIRST+(<statement> --> write left_parenthesis <expression> right_parenthesis semicolon) --> {write}
    FIRST+(<statement> --> print left_parenthesis STRING right_parenthesis semicolon) --> {print}

25. <statement z>
    FIRST - {left_bracket, left_parenthesis, equal_sign}
    FOLLOW - {right_brace, ID, if, while, return, break, continue, read, write, print}

    FIRST+(<statement z> --> <id z> equal_sign <expression> semicolon) -->  {left_bracket, equal_sign}
    FIRST+(<statement z> --> left_parenthesis <expr list> right_parenthesis semicolon) --> {left_parenthesis}


26. <assignment>
    FIRST - {ID}
    FOLLOW - {}

    FIRST+(<assignment> --> <id> equal_sign <expression> semicolon) --> {ID}


27. <func call>
    FIRST - {ID}
    FOLLOW - {}

    FIRST+(<func call> --> ID left_parenthesis <expr list> right_parenthesis semicolon) --> {ID}

28. <expr list>
    FIRST - {empty, ID, NUMBER, minus_sign, left_parenthesis}
    FOLLOW - {right_parenthesis}

    FIRST+(<expr list> --> empty) --> {right_parenthesis}
    FIRST+(<expr list> --> <non-empty expr list>) --> {ID, NUMBER, minus_sign, left_parenthesiss}

29. <non-empty expr list>
    FIRST - {ID, NUMBER, minus_sign, left_parenthesis}
    FOLLOW - {right_parenthesis}

    FIRST+(<non-empty expr list> --> <expression> <non-empty expr list prime>) --> {ID, NUMBER, minus_sign, left_parenthesis}


30. <non-empty expr list prime>
    FIRST - {empty, comma}
    FOLLOW - {right_parenthesis}

    FIRST+(<non-empty expr list prime> --> empty) --> {right_parenthesis}
    FIRST+(<non-empty expr list prime> --> comma <expression> <non-empty expr list prime>) --> {comma}

31. <if statement>
    FIRST - {if}
    FOLLOW - {right_brace, ID, if, while, return, break, continue, read, write, print}

    FIRST+(<if statement> --> if left_parenthesis <condition expression> right_parenthesis <block statements>) --> {if}

32. <condition expression>
    FIRST - {ID, NUMBER, minus_sign, left_parenthesis}
    FOLLOW - {right_parenthesis}

    FIRST+(<condition expression> -->  <condition> <condition expression z>) --> {ID, NUMBER, minus_sign, left_parenthesis}


33. <condition expression z>
    FIRST - {empty, double_and_sign, double_or_sign}
    FOLLOW - {right_parenthesis}

    FIRST+(<condition expression z> --> empty) --> {right_parenthesis}
    FIRST+(<condition expression z> --> <condition op> <condition>) --> {double_and_sign, double_or_sign}

34. <condition op>
    FIRST - {double_and_sign, double_or_sign}
    FOLLOW - {ID, NUMBER, minus_sign, left_parenthesis} 

    FIRST+(<comparison op> --> double_and_sign) --> {double_and_sign}
    FIRST+(<comparison op> --> double_or_sign) --> {double_or_sign}


35. <condition>
    FIRST - {ID, NUMBER, minus_sign, left_parenthesis}
    FOLLOW - {double_and_sign, double_or_sign, right_parenthesis}

    FIRST+(<condition> --> <expression> <comparison op> <expression>) --> {ID, NUMBER, minus_sign, left_parenthesis}


36. <comparison op>
    FIRST - {==, !=, >, >=, <, <=}
    FOLLOW - {ID, NUMBER, minus_sign, left_parenthesis}

    FIRST+(<comparison op> --> ==) --> {==}
    FIRST+(<comparison op> --> !=) --> {!=}
    FIRST+(<comparison op> --> >) --> {>}
    FIRST+(<comparison op> --> >=) --> {>=}
    FIRST+(<comparison op> --> <) --> {<}
    FIRST+(<comparison op> --> <=) --> {<=}


37. <while statement>
    FIRST - {while}
    FOLLOW - {right_brace, ID, if, while, return, break, continue, read, write, print}

    FIRST+(<while statement> --> while left_parenthesis <condition expression> right_parenthesis <block statements>) --> {while}


38. <return statement>
    FIRST - {return}
    FOLLOW - {right_brace, ID, if, while, return, break, continue, read, write, print}

    FIRST+(<return statement> --> return <return statement z>) --> {return}

39. <return statement z>
    FIRST - {ID, NUMBER, minus_sign, left_parenthesis, semicolon}
    FOLLOW - {right_brace, ID, if, while, return, break, continue, read, write, print}

    FIRST+(<return statement z> --> <expression> semicolon) --> {ID, NUMBER, minus_sign, left_parenthesis}
    FIRST+(<return statement z> --> semicolon) --> {semicolon}


40. <break statement>
    FIRST - {break}
    FOLLOW - {right_brace, ID, if, while, return, break, continue, read, write, print}

    FIRST+(<break statement> ---> break semicolon) --> {break}


41. <continue statement>
    FIRST - {continue}
    FOLLOW - {right_brace, ID, if, while, return, break, continue, read, write, print}

    FIRST+(<continue statement> ---> continue semicolon) --> {continue}

42. <expression>
    FIRST - {ID, NUMBER, minus_sign, left_parenthesis}
    FOLLOW - {right_bracket, ==, !=, >, >=, <, <=, semicolon, right_parenthesis, comma, double_and_sign, double_or_sign}

    FIRST+(<expression> --> <term> <expression prime>) --> {ID, NUMBER, minus_sign, left_parenthesis}


43. <expression prime>
    FIRST - {empty, plus_sign, minus_sign}
    FOLLOW - {right_bracket, ==, !=, >, >=, <, <=, semicolon, right_parenthesis, comma, right_parenthesis, double_and_sign, double_or_sign}

    FIRST+(<expression prime> --> empty) --> {right_bracket, ==, !=, >, >=, <, <=, semicolon, right_parenthesis, comma, right_parenthesis, double_and_sign, double_or_sign}
    FIRST+(<expression prime> --> <addop> <term> <expression prime>) --> {plus_sign, minus_sign}


44. <addop>
    FIRST - {plus_sign, minus_sign}
    FOLLOW - {ID, NUMBER, minus_sign, left_parenthesis}

    FIRST+(<addop> --> plus_sign) --> {plus_sign}
    FIRST+(<addop> --> minus_sign) --> {minus_sign}

45. <term>
    FIRST - {ID, NUMBER, minus_sign, left_parenthesis}
    FOLLOW - {plus_sign, mius_sign, right_bracket, ==, !=, >, >=, <, <=, semicolon, right_parenthesis, comma, right_parenthesis, double_and_sign, double_or_sign}

    FIRST+(<term> --> <factor> <term prime>) --> {ID, NUMBER, minus_sign, left_parenthesis}

46. <term prime>
    FIRST - {empty, star_sign, forward_slash}
    FOLLOW - {plus_sign, mius_sign, right_bracket, ==, !=, >, >=, <, <=, semicolon, right_parenthesis, comma, right_parenthesis, double_and_sign, double_or_sign}

    FIRST+(<term prime> --> empty) --> {plus_sign, mius_sign, right_bracket, ==, !=, >, >=, <, <=, semicolon, right_parenthesis, comma, right_parenthesis, double_and_sign, double_or_sign}
    FIRST+(<term prime> --> <mulop> <factor> <term prime>) --> {star_sign, forward_slash}


47. <mulop>
    FIRST - {star_sign, forward_slash}
    FOLLOW - {ID, NUMBER, minus_sign, left_parenthesis}

    FIRST+(<mulop> --> star_sign)--> {star_sign}
    FIRST+(<mulop> --> forward_slash) --> {forward_slash}


48. <factor>
    FIRST - {ID, NUMBER, minus_sign, left_parenthesis}
    FOLLOW - {star_sign, forward_slash, plus_sign, mius_sign, right_bracket, ==, !=, >, >=, <, <=, semicolon, right_parenthesis, comma, right_parenthesis, double_and_sign, double_or_sign}

    FIRST+(<factor> --> ID <factor z>) --> {ID}
    FIRST+(<factor> --> NUMBER) --> {NUMBER}
    FIRST+(<factor> --> minus_sign NUMBER) --> {minus_sign}
    FIRST+(<factor> --> left_parenthesis <expression> right_parenthesis) --> {left_parenthesis}

49. <factor z>
    FIRST - {empty, left_bracket, left_parenthesis}
    FOLLOW - {star_sign, forward_slash, plus_sign, mius_sign, right_bracket, ==, !=, >, >=, <, <=, semicolon, right_parenthesis, comma, right_parenthesis, double_and_sign, double_or_sign}

    FIRST+(<factor z> --> empty) --> {star_sign, forward_slash, plus_sign, mius_sign, right_bracket, ==, !=, >, >=, <, <=, semicolon, right_parenthesis, comma, right_parenthesis, double_and_sign, double_or_sign}
    FIRST+(<factor z> --> left_bracket <expression> right_bracket) --> {left_bracket}
    FIRST+(<factor z> --> left_parenthesis <expr list> right_parenthesis) --> {left_parenthesis}

It has been proved above that the FIRST+ sets of each production rule for each non-terminal in the grammar is disjoint. Thus, the grammar is LL(1).


B. How to compile and run:
==========================

The source consists of two python files named Parser.py and Scanner.py. The scanner is the slightly modified scanner submitted for the scanner project previously, the modifications are just so that it can be used by the parser I wrote.

The program doesn't need to be compiled since it is written in python.

To run the program :-

1. Place the submitted Parser.py and Scanner.py in the same folder.

2. Open terminal (or command line) and type the following:

    python Parser.py /path/to/input/file

    If the input file is a directory, or does not exist, or can not be read, the program will show error and quit. Trying to run the program without an input file will also quit the program. 

3. The output is either 'pass' or 'error' from the parser. Scanner errors are prefixed by 'Error in Scanner'.

4. If the input program is parsed successfully according to the grammar above, it will also show the variable count (global and local), function definition count (not function declarations), and the number of statements according to the <statements> rule in the above grammar.

5. If the input program parsing is unsuccessful, it will output 'error'.

6. The parser has been tested in the CSC512 VCL environment.


C. Program characteristics:
===========================

1. I have implemented a recursive descent parser. Each non-terminal symbol in the grammar (see list above) has it's own method in the code, which recursively expands the corresponding rules. 

2. Every non-terminal symbol's function expands based on the next token read from the scanner. If the function is able to expand the rule successfully it returns true, otherwise false.

3. The program terminates when the starting non-terminal's function returns. The first non-terminal's function returns True if all the rules have been expanded correctly and the input file token being read is end of file (''). If it returns True, it means that the parser has completed successfully, else it means that it has failed. 

4. The program counts the number of global and local variables using a counter which is incremented in the non-terminals <data decls>, <data decls new> and <id list prime> whenever a variable declaration is encountered.

5. The program counts the number of functions (not function declarations) using a counter which is incremented in the non-terminal <func_z>.

6. The program counts the number of statements using a counter which is incremented in the <statement> non-terminal's function.









