// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 100000;

// Hash table
node *table[N];

//initiate dictionary size
int dict_size = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    int index = hash(word);

    node *n = table[index];

    while (n != NULL)
    {
        if (strcasecmp(word, n->word) == 0)
        {
            return true;
        }
        n = n->next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // Function by joseph robinson
    // This hash function adds the ASCII values of all characters in the word together
    long sum = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        sum += tolower(word[i]);
    }
    return sum % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    FILE *input = fopen(dictionary, "r");

    if (input == NULL)
    {
        fclose(input);
        return false;
    }

    char buffer[LENGTH + 1];

    while (fscanf(input, "%s", buffer) != EOF)
    {
        node *new_word = malloc(sizeof(node));

        if (new_word == NULL)
        {
            return false;
        }

        //copy string into node
        strcpy(new_word->word, buffer);
        new_word->next = NULL;

        //find hash index
        int index = hash(buffer);

        //add node to hash index
        new_word->next = table[index];
        table[index] = new_word;
        dict_size++;
    }
    fclose(input);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return dict_size;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        node *n = table[i];

        while (n != NULL)
        {
            node *temp = n;

            n = n->next;

            free(temp);
        }

        while (n == NULL && i == N - 1)
        {
            return true;
        }
    }
    return false;
}
