
#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)

int add(int a) {
int local[3];
local[0] = a;
read(local[1]);
local[2] = local[0] + local[1];
return local[2];
}

int main() {
int local[3];
read(local[0]);
local[2] = add(local[0]);
write( local[2]);
}
