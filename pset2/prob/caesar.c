//includes
#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{
    // key value from command line argument
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    for (int i = 0, n = strlen(argv[1]); i < n; i++)
    {
        if (isalpha(argv[1][i]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }

    // taking key and to stop overflow of int
    int key = atoi(argv[1]) % 26;

    //input plaintext
    string plain = get_string("plaintext: ");

    //encrypt plaintext
    for (int j = 0, o = strlen(plain); j < o; j++)
    {
        if (isupper(plain[j]))
        {
            plain[j] = ((plain[j] - 'A') + key) % 26 + 'A';
        }
        else if (islower(plain[j]))
        {
            plain[j] = ((plain[j] - 'a') + key) % 26 + 'a';
        }
    }
    //output ciphertext
    printf("ciphertext: %s\n", plain);
    return 0;
}