#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)
int main() {    int csc512a, csc512sum;    read(csc512a);    csc512sum = 0;    while (csc512a>0) {        csc512sum = csc512sum + csc512a;        csc512a = csc512a - 1;    }    write(csc512sum);}