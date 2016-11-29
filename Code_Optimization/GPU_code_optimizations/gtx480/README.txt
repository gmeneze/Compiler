Included Files in this folder :-
1. opt1.cu   — Loop unrolling (explained in report)
2. opt2.cu   - Memory Optimization (explained in report)
3. opt3.cu   - Thread Divergence minimization (explained in report)
4. opt4.cu   - Device constant (explained in report)
5. optAll.cu  - All above optimizations combined.
6. Makefile - To compile and clean

How to Compile :-
————————————————
1. Login to GTX480 or GTX780 machine on ARC cluster.

2. Run clean :-
   make clean

3. Run the following commands ($ represents unix command prompt) :-
   $ make opt1
   $ make opt2
   $ make opt3
   $ make opt4
   $ make optAll

How to run :-
—————————————
1. Run using the following commands from the folder where the code was compiled ($ represents unix command prompt) :-
   $ ./opt1
   $ ./opt2
   $ ./opt3
   $ ./opt4
   $ ./opt5
   


