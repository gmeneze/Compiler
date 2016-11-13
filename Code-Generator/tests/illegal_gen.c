#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)
#define print(x) printf(x)

int global[8];


void populate_arrays(void)
{
int local[8];
local[0] = 0 + 0;
global[ local[0]] = 0;
local[1] = 0 + 1;
global[ local[1]] = 1;
local[2] = 0 + 2;
global[ local[2]] = 1;
local[3] = 0 + 3;
global[ local[3]] = 2;
local[4] = 4 + 0;
global[ local[4]] = 3;
local[5] = 4 + 1;
global[ local[5]] = 5;
local[6] = 4 + 2;
global[ local[6]] = 8;
local[7] = 4 + 3;
global[ local[7]] = 13;
}

int main(void)
{
int local[4];
populate_arrays();
local[0] = 0;
local[1] = 8;
print("The first few digits of the Fibonacci sequence are:\n");
c0:;

if ( local[0] < local[1])goto c1;
goto c2;
c1:;

local[2] = 0 + local[0];
local[2] = global[local[2]];
write( local[2]);
local[3] = local[0] + 1;
local[0] = local[3];
goto c0;
c2:;

}
