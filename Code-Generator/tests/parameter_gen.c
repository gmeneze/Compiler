#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)


void foo(int m,int n) {
int local[4];
local[0] = m;
local[1] = n;
local[2] = local[0] + local[1];
local[0] = local[2];
local[3] = local[1] + local[0];
local[1] = local[3];
}

int main() {
int local[1];
read(local[0]);
foo( local[0], local[0]);
write( local[0]);
}
