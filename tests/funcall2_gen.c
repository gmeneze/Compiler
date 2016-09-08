#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)
#define print(x) printf(x)
int csc512c(){    return 1;}int csc512b(){    return 2;}int csc512a(){    return 3;}int csc512foo(int csc512a, int csc512b, int csc512c){    return (csc512a*3 + csc512b*2 + csc512c);}int main() {    int csc512val;    csc512val = csc512foo(csc512a(), csc512b(), csc512c());    print("I calculate the answer to be: ");    write(csc512val);}