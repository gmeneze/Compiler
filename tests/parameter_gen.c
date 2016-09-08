#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)
void csc512foo(int csc512m,int csc512n) {    csc512m = csc512m + csc512n;    csc512n = csc512n + csc512m;}int main() {    int csc512a;    read(csc512a);    csc512foo(csc512a,csc512a);    write(csc512a);}