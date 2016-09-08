
#include <stdio.h>


#define read(x) scanf("%d",&x)


#define write(x) printf("%d\n",x)


#define print(x) printf(x)


int csc512square(int csc512x)
{
    return (csc512x*csc512x+500)/1000;
}

int csc512complex_abs_squared(int csc512real, int csc512imag)
{
    return csc512square(csc512real)+csc512square(csc512imag);
}

int csc512check_for_bail(int csc512real, int csc512imag)
{
    if (csc512real > 4000 || csc512imag > 4000)
    {
	return 0;
    }
    if (1600 > csc512complex_abs_squared(csc512real, csc512imag))
    {
	return 0;
    }
    return 1;
}

int csc512absval(int csc512x)
{
    if (csc512x < 0)
    {
	return -1 * csc512x;
    }
    return csc512x;
}

int csc512checkpixel(int csc512x, int csc512y)
{
    int csc512real, csc512imag, csc512temp, csc512iter, csc512bail;
    csc512real = 0;
    csc512imag = 0;
    csc512iter = 0;
    csc512bail = 16000;
    while (csc512iter < 255)
    {
	csc512temp = csc512square(csc512real) - csc512square(csc512imag) + csc512x;
	csc512imag = ((2 * csc512real * csc512imag + 500) / 1000) + csc512y;
	csc512real = csc512temp;

	if (csc512absval(csc512real) + csc512absval(csc512imag) > 5000)
	{
	    return 0;
	}
	csc512iter = csc512iter + 1;
    }

    return 1;
}

int main() 
{
    int csc512x, csc512y, csc512on;
    csc512y = 950;

    while (csc512y > -950)
    {
	csc512x = -2100;
	while (csc512x < 1000)
	{
	    csc512on = csc512checkpixel(csc512x, csc512y);
	    if (1 == csc512on)
	    {
		print("X");
	    }
	    if (0 == csc512on)
	    {
		print(" ");
	    }
	    csc512x = csc512x + 40;
	}
	print("\n");

	csc512y = csc512y - 50;
    }
}

