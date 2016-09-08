
#include <stdio.h>


#define read(x) scanf("%d",&x)


#define write(x) printf("%d\n",x)


#define print(x) printf(x)


int csc512array_1[4]; 
//glen here

int csc512array_2[4];

void csc512populate_arrays(void)
{
    csc512array_1[0] = 0;
    csc512array_1[1] = 1;
    csc512array_1[2] = 1;
    csc512array_1[3] = 2;

    csc512array_2[0] = 3;
    csc512array_2[1] = 5;
    csc512array_2[2] = 8;
    csc512array_2[3] = 13;
}

int main(void)
{
    int csc512idx, csc512bound;

    csc512populate_arrays();
    
    csc512idx = 0;
    csc512bound = 8;

    print("The first few digits of the Fibonacci sequence are:\n");
    while (csc512idx < csc512bound)
    {
	write(csc512array_1[csc512idx]);
	csc512idx = csc512idx + 1;
    }
}
