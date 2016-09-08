
#include <stdio.h>


#define read(x) scanf("%d",&x)


#define write(x) printf("%d\n",x)


int main() {
    int csc512a, csc512sum;
    read(csc512a);
    csc512sum = (csc512a+1) *csc512a / 2;
    write(csc512sum);
}
