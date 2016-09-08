
#include <stdio.h>


#define read(x) scanf("%d",&x)


#define write(x) printf("%d\n",x)


#define print(x) printf(x)


int csc512getinput(void)
{
    int csc512a;
    csc512a = -1;
    while (0 > csc512a)
    {
	read(csc512a);
	if (0 > csc512a)
	{
	    print("I need a non-negative number: ");
	}
    }

    return csc512a;
}

int main() 
{
    int csc512line1, csc512line2, csc512line3, csc512line4, csc512line5, csc512line6, csc512line7, csc512line8, csc512line9, 
	csc512line10, csc512line11, csc512line12, csc512dependant, csc512single, csc512a, csc512b, csc512c, csc512d, csc512e, csc512f, csc512g, 
	csc512eic, csc512spousedependant;

    print("Welcome to the United States 1040 federal income tax program.\n");
    print("(Note: this isn't the real 1040 form. If you try to submit your\n");
    print("taxes this way, you'll get what you deserve!\n\n");

    print("Answer the following questions to determine what you owe.\n\n");

    print("Total wages, salary, and tips? ");
    csc512line1 = csc512getinput();
    print("Taxable interest (such as from bank accounts)? ");
    csc512line2 = csc512getinput();
    print("Unemployment compensation, qualified state tuition, and Alaska\n");
    print("Permanent Fund dividends? ");
    csc512line3 = csc512getinput();
    csc512line4 = csc512line1+csc512line2+csc512line3;
    print("Your adjusted gross income is: ");
    write(csc512line4);

    print("Enter <1> if your parents or someone else can claim you on their");
    print(" return. \nEnter <0> otherwise: ");
    csc512dependant = csc512getinput();
    if (0 != csc512dependant)
    {
	csc512a = csc512line1 + 250;
	csc512b = 700;
	csc512c = csc512b;
	if (csc512c < csc512a)
	{
	    csc512c = csc512a;
	}
	print("Enter <1> if you are single, <0> if you are married: ");
	csc512single = csc512getinput();
	if (0 != csc512single)
	{
	    csc512d = 7350;
	}
	if (0 == csc512single)
	{
	    csc512d = 4400;
	}
	csc512e = csc512c;
	if (csc512e > csc512d)
	{
	    csc512e = csc512d;
	}
	csc512f = 0;
	if (csc512single == 0)
	{
	    print("Enter <1> if your spouse can be claimed as a dependant, ");
	    print("enter <0> if not: ");
	    csc512spousedependant = csc512getinput();
	    if (0 == csc512spousedependant)
	    {
		csc512f = 2800;
	    }
	}
	csc512g = csc512e + csc512f;

	csc512line5 = csc512g;
    }
    if (0 == csc512dependant)
    {
	print("Enter <1> if you are single, <0> if you are married: ");
	csc512single = csc512getinput();
	if (0 != csc512single)
	{
	    csc512line5 = 12950;
	}
	if (0 == csc512single)
	{
	    csc512line5 = 7200;
	}
    }

    csc512line6 = csc512line4 - csc512line5;
    if (csc512line6 < 0)
    {
	csc512line6 = 0;
    }
    print("Your taxable income is: ");
    write(csc512line6);

    print("Enter the amount of Federal income tax withheld: ");
    csc512line7 = csc512getinput();
    print("Enter <1> if you get an earned income credit (EIC); ");
    print("enter 0 otherwise: ");
    csc512eic = csc512getinput();
    csc512line8 = 0;
    if (0 != csc512eic)
    {
	print("OK, I'll give you a thousand dollars for your credit.\n");
	csc512line8 = 1000;
    }
    csc512line9 = csc512line8 + csc512line7;
    print("Your total tax payments amount to: ");
    write(csc512line9);

    csc512line10 = (csc512line6 * 28 + 50) / 100;
    print("Your total tax liability is: ");
    write(csc512line10);

    csc512line11 = csc512line9 - csc512line10;
    if (csc512line11 < 0)
    {
	csc512line11 = 0;
    }
    if (csc512line11 > 0)
    {
	print("Congratulations, you get a tax refund of $");
	write(csc512line11);
    }

    csc512line12 = csc512line10-csc512line9;
    if (csc512line12 >= 0)
    {
	print("Bummer. You owe the IRS a check for $");
	write(csc512line12);
    }
    if (csc512line12 < 0)
    {
	csc512line12 = 0;
    }

    print("Thank you for using ez-tax.\n");
}

