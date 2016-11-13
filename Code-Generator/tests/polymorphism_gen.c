#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)
#define binary int
#define decimal int


void print_two(int a, int b) {
int local[2];
local[0] = a;
local[1] = b; write( local[0]);
write( local[1]);
}

int main() {
int local[2];
read(local[1]);
read(local[0]); print_two( local[1], local[0]);
print_two( local[0], local[1]);
}
