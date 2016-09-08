
#include <stdio.h>


#define read(x) scanf("%d",&x)


#define write(x) printf("%d\n",x)


int csc512recursionsum(int csc512n) {
    if (csc512n==0) {
        return 0;
    }
    return csc512n + csc512recursionsum(csc512n-1);
}

int main() {
    int csc512a;
    read(csc512a);
    write(csc512recursionsum(csc512a));
}


