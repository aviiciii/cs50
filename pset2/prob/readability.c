//includes
#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

// declaration
int count_letters(string text);
int count_words(string text);
int count_sentences(string text);



int main(void)
{
    // prompt input

    string text = get_string("Text: ");

    //count letters
    float x = count_letters(text);

    //count words
    float y = count_words(text);

    //count sentences
    float z = count_sentences(text);

    // find average
    // avg no of letters per 100 words
    float l = x / y * 100;

    // avg no of sentences per 100 words
    float s = z / y * 100;

    //using formula
    float index = 0.0588 * l - 0.296 * s - 15.8;
    int grade = round(index);


    //print result
    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }

    else if (grade > 16)
    {
        printf("Grade 16+\n");
    }

    else
    {
        printf("Grade %i\n", grade);
    }


}



int count_letters(string text)
{
    int letters = 0;

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }
    }
    return letters;
}

int count_words(string text)
{
    int words = 1;

    for (int j = 0, n = strlen(text); j < n; j++)
    {
        if (isspace(text[j]))
        {
            words++;
        }
    }
    return words;
}

int count_sentences(string text)
{
    int sentences = 0;

    for (int k = 0, n = strlen(text); k < n; k++)
    {
        if (text[k] == '.' || text[k] == '?' || text[k] == '!')
        {
            sentences++;
        }

    }
    return sentences;
}