#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)
#define print(x) printf(x)


int c()
{

return 1;
}

int b()
{

return 2;
}

int a()
{

return 3;
}

int foo(int a, int b, int c)
{
int local[7];
local[0] = a;
local[1] = b;
local[2] = c;
local[3] = local[0] * 3;
local[4] = local[1] * 2;
local[5] = local[3] + local[4];
local[6] = local[5] + local[2];
return local[6];
}

int main() 
{
int local[5];
local[1] = c();
local[2] = b();
local[3] = a();
local[4] = foo(local[3],local[2],local[1]);
local[0] = local[4];
print("I calculate the answer to be: ");
write( local[0]);
}
