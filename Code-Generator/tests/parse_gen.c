#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)
#define print(x) printf(x)


void bar(void)
{
int local[2];
if ( local[0] > local[1]) goto c0;
goto c1;
c0:;

return;
c1:;

local[0] = local[1];
return;
}

void foo(void)
{

bar();
}

int main(void)
{