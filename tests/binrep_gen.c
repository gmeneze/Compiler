#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)
#define print(x) printf(x)
void csc512recursedigit(int csc512n) {    int csc512on;    if (0 == csc512n) {	return;    }    csc512on = 0;    if (0 != (csc512n-((csc512n/2)*2))) {        csc512on = 1;    }    csc512recursedigit(csc512n/2);    if (0 == csc512on) {	print("0");    }    if (1 == csc512on) {	print("1");    }}int main() {    int csc512a;    csc512a = 0;    while (0 >= csc512a) {	print("Give me a number: ");	read(csc512a);		if (0 >= csc512a) {	    print("I need a positive integer.\n");	}    }    print("The binary representation of: ");    write(csc512a);    print("is: ");    csc512recursedigit(csc512a);    print("\n\n");}