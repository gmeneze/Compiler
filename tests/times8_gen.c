#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)
int csc512add(int csc512a, int csc512b) {  return csc512a+csc512b;}int csc512times_eight(int csc512a) {  return csc512add(csc512add(csc512add(csc512a,csc512a),csc512add(csc512a,csc512a)), csc512add(csc512add(csc512a,csc512a),csc512add(csc512a,csc512a)));}int main() {    int csc512a, csc512b;    read(csc512a);    write(csc512times_eight(csc512a));}