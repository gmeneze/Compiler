#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)


int main() {
int local[2];
read(local[0]);
read(local[1]);
if ( local[0]>= local[1])goto c0;
goto c1;
c0:;
 write( local[0]);
c1:;

if ( local[1]> local[0])goto c2;
goto c3;
c2:;
 write( local[1]);
c3:;

}
