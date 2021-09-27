#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // prompt for height

    int n;

    do
    {
        n = get_int("Height: ");
    }

    while (n < 1 || n > 8);

    // dots (change to spaces) and hash

    n = n + 1 ;

    int i;
    int j;

    // vertical condition
    for (i = 1; i < n; i++)
    {
        // horizontal condition
        for (j = 0; j < n - 1; j++)
        {
            // condition for spaces
            if (i + j < n - 1)

                printf(" ");

            else
                printf("#");
        }

        printf("\n");
    }

}