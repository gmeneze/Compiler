#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)
int csc512max(int csc512a, int csc512b) {    if (csc512a>csc512b) {        return csc512a;    }    return csc512b;}int main() {    int csc512a,csc512b;    read(csc512a);    read(csc512b);    write(csc512max(csc512a,csc512b));}