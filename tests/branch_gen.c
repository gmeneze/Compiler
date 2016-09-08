#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)
int main() {    int csc512a, csc512b;    read(csc512a);    read(csc512b);    if (csc512a>=csc512b) {        write(csc512a);    }    if (csc512b>csc512a) {        write(csc512b);    }}