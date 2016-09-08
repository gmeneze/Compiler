
#include <stdio.h>


#define read(x) scanf("%d",&x)


#define write(x) printf("%d\n",x)


#define print(x) printf(x)


int csc512array[16];

void csc512initialize_array(void)
{
    int csc512idx, csc512bound;
    csc512bound = 16;

    csc512idx = 0;
    while (csc512idx < csc512bound)
    {
	csc512array[csc512idx] = -1;
	csc512idx = csc512idx + 1;
    }
}

int csc512fib(int csc512val)
{
    if (csc512val < 2)
    {
	return 1;
    }
    if (csc512array[csc512val] == -1)
    {
	csc512array[csc512val] = csc512fib(csc512val - 1) + csc512fib(csc512val - 2);
    }

    return csc512array[csc512val];
}

int main(void)
{
    int csc512idx, csc512bound;
    csc512bound = 16;

    csc512initialize_array();
    
    csc512idx = 0;

    print("The first few digits of the Fibonacci sequence are:\n");
    while (csc512idx < csc512bound)
    {
	write(csc512fib(csc512idx));
	csc512idx = csc512idx + 1;
    }
}
