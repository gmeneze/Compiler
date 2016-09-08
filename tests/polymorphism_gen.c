#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)
#define binary int
#define decimal int
void csc512print_two(int csc512a, int csc512b) {      write(csc512a);    write(csc512b);}int main() {    binary csc512b;    decimal csc512a;    read(csc512a);    read(csc512b);      csc512print_two(csc512a, csc512b);    csc512print_two(csc512b, csc512a);}