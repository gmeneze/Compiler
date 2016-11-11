
#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)
#define print(x) printf(x)

int g()
{

return 1;
}

int f()
{
int local[2];
local[0] = g();
local[1] = local[0] + 1;
return local[1];
}

int e()
{
int local[2];
local[0] = f();
local[1] = local[0] + 1;
return local[1];
}

int d()
{
int local[2];
local[0] = e();
local[1] = local[0] + 1;
return local[1];
}

int c()
{
int local[2];
local[0] = d();
local[1] = local[0] + 1;
return local[1];
}

int b()
{
int local[2];
local[0] = c();
local[1] = local[0] + 1;
return local[1];
}

int a()
{
int local[2];
local[0] = b();
local[1] = local[0] + 1;
return local[1];
}

int main() 
{
int local[2];
local[1] = a();
local[0] = local[1];
print("I calculate the answer to be: ");
write( local[0]);
}
