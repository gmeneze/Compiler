#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)


int max(int a, int b) {
int local[2];
local[0] = a;
local[1] = b;
if ( local[0]> local[1]) goto c0;
goto c1;
c0:;
 return local[0];
c1:;

return local[1];
}

int main() {
int local[3];
read(local[0]);
read(local[1]);
local[2] = max(local[0],local[1]);
write( local[2]);
}
