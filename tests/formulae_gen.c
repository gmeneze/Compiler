
#include <stdio.h>


#define read(x) scanf("%d",&x)


#define write(x) printf("%d\n",x)


#define print(x) printf(x)


int csc512getinput(void)
{
    int csc512a;
    csc512a = 0;
    while (0 >= csc512a)
    {
	read(csc512a);
	if (0 > csc512a)
	{
	    print("I need a positive number: ");
	}
    }

    return csc512a;
}

int main() 
{
    int csc512coneradius, csc512coneheight;
    int csc512circleradius;
    int csc512trianglebase, csc512triangleheight;
    int csc512sphereradius;

    int csc512cone, csc512circle, csc512triangle, csc512sphere;
    int csc512pi;
    csc512pi = 3141;

    print("Give me a radius for the base of a cone: ");
    csc512coneradius = csc512getinput();
    print("Give me a height for a cone: ");
    csc512coneheight = csc512getinput();
    print("Give me a radius for a circle: ");
    csc512circleradius = csc512getinput();
    print("Give me a length for the base of a triangle: ");
    csc512trianglebase = csc512getinput();
    print("Give me a height for a triangle: ");
    csc512triangleheight = csc512getinput();
    print("Give me a radius for a sphere: ");
    csc512sphereradius = csc512getinput();

    csc512cone = (csc512pi*csc512coneradius*csc512coneradius*csc512coneheight + 500) / 3000;
    csc512circle = (csc512pi*csc512circleradius*csc512circleradius + 500) / 1000;
    csc512triangle = (csc512trianglebase*csc512triangleheight) / 2;
    csc512sphere = (4*csc512pi*csc512sphereradius*csc512sphereradius*csc512sphereradius+500) / 3000;

    print("The volume of the cone is: ");
    write(csc512cone);
    print("The area of the circle is: ");
    write(csc512circle);
    print("The area of the triangle is: ");
    write(csc512triangle);
    print("The volume of the sphere is: ");
    write(csc512sphere);
}
