#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)


int main() {
int local[4];
read(local[0]);
local[1] = 0;
c0:;

if ( local[0]> 0)goto c1;
goto c2;
c1:;
 local[2] = local[1] + local[0];
local[1] = local[2];
local[3] = local[0] - 1;
local[0] = local[3];
goto c0;
c2:;

write( local[1]);
}
