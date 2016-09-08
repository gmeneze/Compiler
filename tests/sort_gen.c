
#include <stdio.h>


#define read(x) scanf("%d",&x)


#define write(x) printf("%d\n",x)


#define print(x) printf(x)


int csc512array_1[16];
int csc512array_2[16];
int csc512array_3[16];
int csc512array_4[16];

void csc512populate_arrays(void)
{
    csc512array_1[0] = 0; csc512array_2[0] = 15; csc512array_3[0] = 5; csc512array_4[0] = 13;
    csc512array_1[1] = 1; csc512array_2[1] = 14; csc512array_3[1] = 5; csc512array_4[1] = 9;
    csc512array_1[2] = 2; csc512array_2[2] = 13; csc512array_3[2] = 5; csc512array_4[2] = 12;
    csc512array_1[3] = 3; csc512array_2[3] = 12; csc512array_3[3] = 5; csc512array_4[3] = 1;
    csc512array_1[4] = 4; csc512array_2[4] = 11; csc512array_3[4] = 5; csc512array_4[4] = 0;
    csc512array_1[5] = 5; csc512array_2[5] = 10; csc512array_3[5] = 5; csc512array_4[5] = 14;
    csc512array_1[6] = 6; csc512array_2[6] = 9; csc512array_3[6] = 5; csc512array_4[6] = 3;
    csc512array_1[7] = 7; csc512array_2[7] = 8; csc512array_3[7] = 5; csc512array_4[7] = 2;
    csc512array_1[8] = 8; csc512array_2[8] = 7; csc512array_3[8] = 5; csc512array_4[8] = 11;
    csc512array_1[9] = 9; csc512array_2[9] = 6; csc512array_3[9] = 5; csc512array_4[9] = 8;
    csc512array_1[10] = 10; csc512array_2[10] = 5; csc512array_3[10] = 5; csc512array_4[10] = 6;
    csc512array_1[11] = 11; csc512array_2[11] = 4; csc512array_3[11] = 5; csc512array_4[11] = 4;
    csc512array_1[12] = 12; csc512array_2[12] = 3; csc512array_3[12] = 5; csc512array_4[12] = 5;
    csc512array_1[13] = 13; csc512array_2[13] = 2; csc512array_3[13] = 5; csc512array_4[13] = 10;
    csc512array_1[14] = 14; csc512array_2[14] = 1; csc512array_3[14] = 5; csc512array_4[14] = 7;
    csc512array_1[15] = 15; csc512array_2[15] = 0; csc512array_3[15] = 5; csc512array_4[15] = 15;
}

void csc512print_arrays(void)
{
    int csc512idx, csc512bound;
    csc512bound = 16;
    print("Array_1:\n");
    csc512idx = 0;
    while (csc512idx < csc512bound)
    {
	write(csc512array_1[csc512idx]);
	csc512idx = csc512idx + 1;
    }

    print("\nArray_2:\n");
    csc512idx = 0;
    while (csc512idx < csc512bound)
    {
	write(csc512array_2[csc512idx]);
	csc512idx = csc512idx + 1;
    }

    print("\nArray_3:\n");
    csc512idx = 0;
    while (csc512idx < csc512bound)
    {
	write(csc512array_3[csc512idx]);
	csc512idx = csc512idx + 1;
    }

    print("\nArray_4:\n");
    csc512idx = 0;
    while (csc512idx < csc512bound)
    {
	write(csc512array_4[csc512idx]);
	csc512idx = csc512idx + 1;
    }
    print("\n");    
}

int main() 
{
    int csc512idx, csc512bound, csc512temp;
    csc512bound = 16;

    csc512populate_arrays();
    csc512print_arrays();

    csc512bound = 16;

    csc512idx = 0;
    while (csc512idx < csc512bound - 1)
    {
	if (csc512array_1[csc512idx] > csc512array_1[csc512idx + 1])
	{
	    csc512temp = csc512array_1[csc512idx];
	    csc512array_1[csc512idx] = csc512array_1[csc512idx + 1];
	    csc512array_1[csc512idx + 1] = csc512temp;
	    csc512idx = 0;
	    continue;
	}
	
	csc512idx = csc512idx + 1;
    }

    csc512idx = 0;
    while (csc512idx < csc512bound - 1)
    {
	if (csc512array_2[csc512idx] > csc512array_2[csc512idx + 1])
	{
	    csc512temp = csc512array_2[csc512idx];
	    csc512array_2[csc512idx] = csc512array_2[csc512idx + 1];
	    csc512array_2[csc512idx + 1] = csc512temp;
	    csc512idx = 0;
	    continue;
	}
	
	csc512idx = csc512idx + 1;
    }


    csc512idx = 0;
    while (csc512idx < csc512bound - 1)
    {
	if (csc512array_3[csc512idx] > csc512array_3[csc512idx + 1])
	{
	    csc512temp = csc512array_1[csc512idx];
	    csc512array_3[csc512idx] = csc512array_3[csc512idx + 1];
	    csc512array_3[csc512idx + 1] = csc512temp;
	    csc512idx = 0;
	    continue;
	}
	
	csc512idx = csc512idx + 1;
    }

    csc512idx = 0;
    while (csc512idx < csc512bound - 1)
    {
	if (csc512array_4[csc512idx] > csc512array_4[csc512idx + 1])
	{
	    csc512temp = csc512array_4[csc512idx];
	    csc512array_4[csc512idx] = csc512array_4[csc512idx + 1];
	    csc512array_4[csc512idx + 1] = csc512temp;
	    csc512idx = 0;
	    continue;
	}
	
	csc512idx = csc512idx + 1;
    }

    csc512print_arrays();
}

