#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)
#define print(x) printf(x)


int getinput(void)
{
int local[1];
local[0] = -1;
c0:;

if ( 0 > local[0]) goto c1;
goto c2;
c1:;

read(local[0]);
if ( 0 > local[0]) goto c3;
goto c4;
c3:;

print("I need a non-negative number: ");
c4:;

goto c0;
c2:;

return local[0];
}

int main() 
{
int local[43];
print("Welcome to the United States 1040 federal income tax program.\n");
print("(Note: this isn't the real 1040 form. If you try to submit your\n");
print("taxes this way, you'll get what you deserve!\n\n");
print("Answer the following questions to determine what you owe.\n\n");
print("Total wages, salary, and tips? ");
local[23] = getinput();
local[0] = local[23];
print("Taxable interest (such as from bank accounts)? ");
local[24] = getinput();
local[1] = local[24];
print("Unemployment compensation, qualified state tuition, and Alaska\n");
print("Permanent Fund dividends? ");
local[25] = getinput();
local[2] = local[25];
local[26] = local[0] + local[1];
local[27] = local[26] + local[2];
local[3] = local[27];
print("Your adjusted gross income is: ");
write( local[3]);
print("Enter <1> if your parents or someone else can claim you on their");
print(" return. \nEnter <0> otherwise: ");
local[28] = getinput();
local[12] = local[28];
if ( 0 != local[12]) goto c5;
goto c6;
c5:;

local[29] = local[0] + 250;
local[14] = local[29];
local[15] = 700;
local[16] = local[15];
if ( local[16] < local[14]) goto c7;
goto c8;
c7:;

local[16] = local[14];
c8:;

print("Enter <1> if you are single, <0> if you are married: ");
local[30] = getinput();
local[13] = local[30];
if ( 0 != local[13]) goto c9;
goto c10;
c9:;

local[17] = 7350;
c10:;

if ( 0 == local[13]) goto c11;
goto c12;
c11:;

local[17] = 4400;
c12:;

local[18] = local[16];
if ( local[18] > local[17]) goto c13;
goto c14;
c13:;

local[18] = local[17];
c14:;

local[19] = 0;
if ( local[13] == 0) goto c15;
goto c16;
c15:;

print("Enter <1> if your spouse can be claimed as a dependant, ");
print("enter <0> if not: ");
local[31] = getinput();
local[22] = local[31];
if ( 0 == local[22]) goto c17;
goto c18;
c17:;

local[19] = 2800;
c18:;

c16:;

local[32] = local[18] + local[19];
local[20] = local[32];
local[4] = local[20];
c6:;

if ( 0 == local[12]) goto c19;
goto c20;
c19:;

print("Enter <1> if you are single, <0> if you are married: ");
local[33] = getinput();
local[13] = local[33];
if ( 0 != local[13]) goto c21;
goto c22;
c21:;

local[4] = 12950;
c22:;

if ( 0 == local[13]) goto c23;
goto c24;
c23:;

local[4] = 7200;
c24:;

c20:;

local[34] = local[3] - local[4];
local[5] = local[34];
if ( local[5] < 0) goto c25;
goto c26;
c25:;

local[5] = 0;
c26:;

print("Your taxable income is: ");
write( local[5]);
print("Enter the amount of Federal income tax withheld: ");
local[35] = getinput();
local[6] = local[35];
print("Enter <1> if you get an earned income credit (EIC); ");
print("enter 0 otherwise: ");
local[36] = getinput();
local[21] = local[36];
local[7] = 0;
if ( 0 != local[21]) goto c27;
goto c28;
c27:;

print("OK, I'll give you a thousand dollars for your credit.\n");
local[7] = 1000;
c28:;

local[37] = local[7] + local[6];
local[8] = local[37];
print("Your total tax payments amount to: ");
write( local[8]);
local[38] = local[5] * 28;
local[39] = local[38] + 50;
local[40] = local[39] / 100;
local[9] = local[40];
print("Your total tax liability is: ");
write( local[9]);
local[41] = local[8] - local[9];
local[10] = local[41];
if ( local[10] < 0) goto c29;
goto c30;
c29:;

local[10] = 0;
c30:;

if ( local[10] > 0) goto c31;
goto c32;
c31:;

print("Congratulations, you get a tax refund of $");
write( local[10]);
c32:;

local[42] = local[9] - local[8];
local[11] = local[42];
if ( local[11] >= 0) goto c33;
goto c34;
c33:;

print("Bummer. You owe the IRS a check for $");
write( local[11]);
c34:;

if ( local[11] < 0) goto c35;
goto c36;
c35:;

local[11] = 0;
c36:;

print("Thank you for using ez-tax.\n");
}
