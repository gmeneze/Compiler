#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)
#define print(x) printf(x)
void csc512bar(void){    int csc512x, csc512y;    if (csc512x > csc512y)    {	return;    }    csc512x = csc512y;    return;}void csc512foo(void){    csc512bar();}int main(void){    int csc512x,csc512y;    print("Calling foo()...\n");    csc512foo();    print("Called foo().\n");    csc512x == csc512y;}