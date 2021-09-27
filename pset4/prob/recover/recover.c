#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // check argc
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    //check valid input jpg
    char *inputfile = argv[1];

    FILE *inptr = fopen(inputfile, "r");

    if (inptr == NULL)
    {
        printf("Unable to open file: %s\n", inputfile);
        return 2;
    }

    // variables
    FILE *outptr = NULL;
    int jpgcounter = 0;
    char filename[8];// ###.jpg/0   8 characters
    BYTE buffer[512];



    while (fread(&buffer, sizeof(buffer), 1, inptr) == 1)
    {
        //read headerfile
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xe0) == 0xe0)
        {
            //close old jpg if opened
            if (jpgcounter != 0)
            {
                fclose(outptr);
            }
            //open new jpg
            sprintf(filename, "%03i.jpg", jpgcounter);
            outptr = fopen(filename, "w");
            jpgcounter++;
        }

        //copy jpg into output
        if (jpgcounter != 0)
        {
            fwrite(&buffer, sizeof(buffer), 1, outptr);
        }
    }
    fclose(inptr);
    fclose(outptr);


    return 0;
}