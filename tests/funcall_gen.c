#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)
#define print(x) printf(x)
int csc512g(){    return 1;}int csc512f(){    return csc512g() + 1;}int csc512e(){    return csc512f() + 1;}int csc512d(){    return csc512e() + 1;}int csc512c(){    return csc512d() + 1;}int csc512b(){    return csc512c() + 1;}int csc512a(){    return csc512b() + 1;}int main() {    int csc512val;    csc512val = csc512a();    print("I calculate the answer to be: ");    write(csc512val);}