#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)
#define print(x) printf(x)

int global[16];


void initialize_array(void)
{
int local[4];
local[1] = 16;
local[0] = 0;
c0:;

if ( local[0] < local[1]) goto c1;
goto c2;
c1:;

local[2] = 0 + local[0];
global[ local[2]] = -1;
local[3] = local[0] + 1;
local[0] = local[3];
goto c0;
c2:;

}

int fib(int val)
{
int local[11];
local[0] = val;
if ( local[0] < 2) goto c3;
goto c4;
c3:;

return 1;
c4:;

local[2] = 0 + local[0];
local[1] = global[local[2]];
if ( local[1] == -1) goto c5;
goto c6;
c5:;

local[3] = 0 + local[0];
local[5] = local[0] - 2;
local[4] = fib(local[5]);
local[7] = local[0] - 1;
local[6] = fib(local[7]);
local[8] = local[6] + local[4];
global[ local[3]] = local[8];
c6:;

local[10] = 0 + local[0];
local[9] = global[local[10]];
return local[9];
}

int main(void)
{
int local[4];
local[1] = 16;
initialize_array();
local[0] = 0;
print("The first few digits of the Fibonacci sequence are:\n");
c7:;

if ( local[0] < local[1]) goto c8;
goto c9;
c8:;

local[2] = fib(local[0]);
write( local[2]);
local[3] = local[0] + 1;
local[0] = local[3];
goto c7;
c9:;

}
