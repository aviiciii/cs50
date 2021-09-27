#include <cs50.h>
#include <math.h>
#include <stdio.h>

int main(void)
{
    // prompt dollar from user

    float d;
    do
    {
        d = get_float("Change owed: ");
    }
    while (d < 0);

    // change dollar to penny(also rounding off)

    float cent = d * 100;

    int c = round(cent);

    printf("%i\n", c);

    //greedy algorithm

    int k;
    int quater;
    int dime;
    int nickel;
    int penny;

    for (quater = c; quater >= 25; quater -= 25)
    {
        k = k + 1;
    }

    for (dime = quater; dime >= 10; dime -= 10)
    {
        k = k + 1;
    }

    for (nickel = dime; nickel >= 5; nickel -= 5)
    {
        k = k + 1;
    }

    for (penny = nickel; penny >= 1; penny -= 1)
    {
        k = k + 1;
    }

    //print coins

    printf("%i\n", k);
}

