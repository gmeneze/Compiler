#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)
#define print(x) printf(x)

int global[64];


void populate_arrays(void)
{
int local[64];
local[0] = 0 + 0;
local[1] = 16 + 0;
local[2] = 32 + 0;
local[3] = 48 + 0;
global[ local[0]] = 0; global[ local[1]] = 15; global[ local[2]] = 5; global[ local[3]] = 13;
local[4] = 0 + 1;
local[5] = 16 + 1;
local[6] = 32 + 1;
local[7] = 48 + 1;
global[ local[4]] = 1; global[ local[5]] = 14; global[ local[6]] = 5; global[ local[7]] = 9;
local[8] = 0 + 2;
local[9] = 16 + 2;
local[10] = 32 + 2;
local[11] = 48 + 2;
global[ local[8]] = 2; global[ local[9]] = 13; global[ local[10]] = 5; global[ local[11]] = 12;
local[12] = 0 + 3;
local[13] = 16 + 3;
local[14] = 32 + 3;
local[15] = 48 + 3;
global[ local[12]] = 3; global[ local[13]] = 12; global[ local[14]] = 5; global[ local[15]] = 1;
local[16] = 0 + 4;
local[17] = 16 + 4;
local[18] = 32 + 4;
local[19] = 48 + 4;
global[ local[16]] = 4; global[ local[17]] = 11; global[ local[18]] = 5; global[ local[19]] = 0;
local[20] = 0 + 5;
local[21] = 16 + 5;
local[22] = 32 + 5;
local[23] = 48 + 5;
global[ local[20]] = 5; global[ local[21]] = 10; global[ local[22]] = 5; global[ local[23]] = 14;
local[24] = 0 + 6;
local[25] = 16 + 6;
local[26] = 32 + 6;
local[27] = 48 + 6;
global[ local[24]] = 6; global[ local[25]] = 9; global[ local[26]] = 5; global[ local[27]] = 3;
local[28] = 0 + 7;
local[29] = 16 + 7;
local[30] = 32 + 7;
local[31] = 48 + 7;
global[ local[28]] = 7; global[ local[29]] = 8; global[ local[30]] = 5; global[ local[31]] = 2;
local[32] = 0 + 8;
local[33] = 16 + 8;
local[34] = 32 + 8;
local[35] = 48 + 8;
global[ local[32]] = 8; global[ local[33]] = 7; global[ local[34]] = 5; global[ local[35]] = 11;
local[36] = 0 + 9;
local[37] = 16 + 9;
local[38] = 32 + 9;
local[39] = 48 + 9;
global[ local[36]] = 9; global[ local[37]] = 6; global[ local[38]] = 5; global[ local[39]] = 8;
local[40] = 0 + 10;
local[41] = 16 + 10;
local[42] = 32 + 10;
local[43] = 48 + 10;
global[ local[40]] = 10; global[ local[41]] = 5; global[ local[42]] = 5; global[ local[43]] = 6;
local[44] = 0 + 11;
local[45] = 16 + 11;
local[46] = 32 + 11;
local[47] = 48 + 11;
global[ local[44]] = 11; global[ local[45]] = 4; global[ local[46]] = 5; global[ local[47]] = 4;
local[48] = 0 + 12;
local[49] = 16 + 12;
local[50] = 32 + 12;
local[51] = 48 + 12;
global[ local[48]] = 12; global[ local[49]] = 3; global[ local[50]] = 5; global[ local[51]] = 5;
local[52] = 0 + 13;
local[53] = 16 + 13;
local[54] = 32 + 13;
local[55] = 48 + 13;
global[ local[52]] = 13; global[ local[53]] = 2; global[ local[54]] = 5; global[ local[55]] = 10;
local[56] = 0 + 14;
local[57] = 16 + 14;
local[58] = 32 + 14;
local[59] = 48 + 14;
global[ local[56]] = 14; global[ local[57]] = 1; global[ local[58]] = 5; global[ local[59]] = 7;
local[60] = 0 + 15;
local[61] = 16 + 15;
local[62] = 32 + 15;
local[63] = 48 + 15;
global[ local[60]] = 15; global[ local[61]] = 0; global[ local[62]] = 5; global[ local[63]] = 15;
}

void print_arrays(void)
{
int local[14];
local[1] = 16;
print("Array_1:\n");
local[0] = 0;
c0:;

if ( local[0] < local[1]) goto c1;
goto c2;
c1:;

local[3] = 0 + local[0];
local[2] = global[local[3]];
write( local[2]);
local[4] = local[0] + 1;
local[0] = local[4];
goto c0;
c2:;

print("\nArray_2:\n");
local[0] = 0;
c3:;

if ( local[0] < local[1]) goto c4;
goto c5;
c4:;

local[6] = 16 + local[0];
local[5] = global[local[6]];
write( local[5]);
local[7] = local[0] + 1;
local[0] = local[7];
goto c3;
c5:;

print("\nArray_3:\n");
local[0] = 0;
c6:;

if ( local[0] < local[1]) goto c7;
goto c8;
c7:;

local[9] = 32 + local[0];
local[8] = global[local[9]];
write( local[8]);
local[10] = local[0] + 1;
local[0] = local[10];
goto c6;
c8:;

print("\nArray_4:\n");
local[0] = 0;
c9:;

if ( local[0] < local[1]) goto c10;
goto c11;
c10:;

local[12] = 48 + local[0];
local[11] = global[local[12]];
write( local[11]);
local[13] = local[0] + 1;
local[0] = local[13];
goto c9;
c11:;

print("\n"); }

int main() 
{
int local[63];
local[1] = 16;
populate_arrays();
print_arrays();
local[1] = 16;
local[0] = 0;
c12:;

local[3] = local[1] - 1;
if ( local[0] < local[3]) goto c13;
goto c14;
c13:;

local[5] = 0 + local[0];
local[4] = global[local[5]];
local[7] = 0 + local[0];
local[8] = local[7] + 1;
local[6] = global[local[8]];
if ( local[4] > local[6]) goto c15;
goto c16;
c15:;

local[10] = 0 + local[0];
local[9] = global[local[10]];
local[2] = local[9];
local[11] = 0 + local[0];
local[13] = 0 + local[0];
local[14] = local[13] + 1;
local[12] = global[local[14]];
global[ local[11]] = local[12];
local[15] = 0 + local[0];
local[16] = local[15] + 1;
global[ local[16]] = local[2];
local[0] = 0;
goto c12;
c16:;

local[17] = local[0] + 1;
local[0] = local[17];
goto c12;
c14:;

local[0] = 0;
c17:;

local[18] = local[1] - 1;
if ( local[0] < local[18]) goto c18;
goto c19;
c18:;

local[20] = 16 + local[0];
local[19] = global[local[20]];
local[22] = 16 + local[0];
local[23] = local[22] + 1;
local[21] = global[local[23]];
if ( local[19] > local[21]) goto c20;
goto c21;
c20:;

local[25] = 16 + local[0];
local[24] = global[local[25]];
local[2] = local[24];
local[26] = 16 + local[0];
local[28] = 16 + local[0];
local[29] = local[28] + 1;
local[27] = global[local[29]];
global[ local[26]] = local[27];
local[30] = 16 + local[0];
local[31] = local[30] + 1;
global[ local[31]] = local[2];
local[0] = 0;
goto c17;
c21:;

local[32] = local[0] + 1;
local[0] = local[32];
goto c17;
c19:;

local[0] = 0;
c22:;

local[33] = local[1] - 1;
if ( local[0] < local[33]) goto c23;
goto c24;
c23:;

local[35] = 32 + local[0];
local[34] = global[local[35]];
local[37] = 32 + local[0];
local[38] = local[37] + 1;
local[36] = global[local[38]];
if ( local[34] > local[36]) goto c25;
goto c26;
c25:;

local[40] = 0 + local[0];
local[39] = global[local[40]];
local[2] = local[39];
local[41] = 32 + local[0];
local[43] = 32 + local[0];
local[44] = local[43] + 1;
local[42] = global[local[44]];
global[ local[41]] = local[42];
local[45] = 32 + local[0];
local[46] = local[45] + 1;
global[ local[46]] = local[2];
local[0] = 0;
goto c22;
c26:;

local[47] = local[0] + 1;
local[0] = local[47];
goto c22;
c24:;

local[0] = 0;
c27:;

local[48] = local[1] - 1;
if ( local[0] < local[48]) goto c28;
goto c29;
c28:;

local[50] = 48 + local[0];
local[49] = global[local[50]];
local[52] = 48 + local[0];
local[53] = local[52] + 1;
local[51] = global[local[53]];
if ( local[49] > local[51]) goto c30;
goto c31;
c30:;

local[55] = 48 + local[0];
local[54] = global[local[55]];
local[2] = local[54];
local[56] = 48 + local[0];
local[58] = 48 + local[0];
local[59] = local[58] + 1;
local[57] = global[local[59]];
global[ local[56]] = local[57];
local[60] = 48 + local[0];
local[61] = local[60] + 1;
global[ local[61]] = local[2];
local[0] = 0;
goto c27;
c31:;

local[62] = local[0] + 1;
local[0] = local[62];
goto c27;
c29:;

print_arrays();
}
