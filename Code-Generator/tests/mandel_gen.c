#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)
#define print(x) printf(x)


int square(int x)
{
int local[4];
local[0] = x;
local[1] = local[0] * local[0];
local[2] = local[1] + 500;
local[3] = local[2] / 1000;
return local[3];
}

int complex_abs_squared(int real, int imag)
{
int local[5];
local[0] = real;
local[1] = imag;
local[2] = square(local[1]);
local[3] = square(local[0]);
local[4] = local[3] + local[2];
return local[4];
}

int check_for_bail(int real, int imag)
{
int local[5];
local[0] = real;
local[1] = imag;
local[2] = local[0] > 4000 ;
local[3] = local[1] > 4000;
if(local[2] || local[3]) goto c0;
goto c1;
c0:;

return 0;
c1:;

local[4] = complex_abs_squared(local[0],local[1]);
if ( 1600 > local[4]) goto c2;
goto c3;
c2:;

return 0;
c3:;

return 1;
}

int absval(int x)
{
int local[2];
local[0] = x;
if ( local[0] < 0) goto c4;
goto c5;
c4:;

local[1] = -1 * local[0];
return local[1];
c5:;

return local[0];
}

int checkpixel(int x, int y)
{
int local[20];
local[0] = x;
local[1] = y;
local[2] = 0;
local[3] = 0;
local[5] = 0;
local[6] = 16000;
c6:;

if ( local[5] < 255) goto c7;
goto c8;
c7:;

local[7] = square(local[3]);
local[8] = square(local[2]);
local[9] = local[8] - local[7];
local[10] = local[9] + local[0];
local[4] = local[10];
local[11] = 2 * local[2];
local[12] = local[11] * local[3];
local[13] = local[12] + 500;
local[14] = local[13] / 1000;
local[15] = local[14] + local[1];
local[3] = local[15];
local[2] = local[4];
local[16] = absval(local[3]);
local[17] = absval(local[2]);
local[18] = local[17] + local[16];
if ( local[18] > 5000) goto c9;
goto c10;
c9:;

return 0;
c10:;

local[19] = local[5] + 1;
local[5] = local[19];
goto c6;
c8:;

return 1;
}

int main() 
{
int local[6];
local[1] = 950;
c11:;

if ( local[1] > -950) goto c12;
goto c13;
c12:;

local[0] = -2100;
c14:;

if ( local[0] < 1000) goto c15;
goto c16;
c15:;

local[3] = checkpixel(local[0],local[1]);
local[2] = local[3];
if ( 1 == local[2]) goto c17;
goto c18;
c17:;

print("X");
c18:;

if ( 0 == local[2]) goto c19;
goto c20;
c19:;

print(" ");
c20:;

local[4] = local[0] + 40;
local[0] = local[4];
goto c14;
c16:;

print("\n");
local[5] = local[1] - 50;
local[1] = local[5];
goto c11;
c13:;

}
