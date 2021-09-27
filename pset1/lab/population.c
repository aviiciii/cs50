#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // TODO: Prompt for start size

    int x;
    do
    {
        x = get_int("Start Size : ");
    }
    while (x < 9) ;


    // TODO: Prompt for end size

    int y;
    do
    {
        y = get_int("End Size : ");

    }
    while (y < x);


    // TODO: Calculate number of years until we reach threshold

    int z;

    for (z = 0; x < y; z++)
    {
        x = x + (x / 3) - (x / 4);
    }


    // TODO: Print number of years

    printf("Years: %i", z);

}