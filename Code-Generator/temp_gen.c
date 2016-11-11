
#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)

int add(int a) {
int local[2];
local[0]=a;
read(local[1]);
return local[0]+local[1];
}

int main() {
int local[2];
read(local[0]);
write(add(local[0]));
}
