#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)


int add(int a, int b) {
int local[3];
local[0] = a;
local[1] = b;
local[2] = local[0] + local[1];
return local[2];
}

int times_eight(int a) {
int local[8];
local[0] = a;
local[1] = add(local[0],local[0]);
local[2] = add(local[0],local[0]);
local[3] = add(local[2],local[1]);
local[4] = add(local[0],local[0]);
local[5] = add(local[0],local[0]);
local[6] = add(local[5],local[4]);
local[7] = add(local[6],local[3]);
return local[7];
}

int main() {
int local[3];
read(local[0]);
local[2] = times_eight(local[0]);
write( local[2]);
}
