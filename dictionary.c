// Implements a dictionary's functionality

#include <cs50.h>
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

int wordCount = 0;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    int key = hash(word);

    node *noden = table[key];

    while (noden != NULL)
    {
        if (strcasecmp(noden->word, word) == 0)
        {
            return true;
        }

        noden = noden->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    int value = 0;

    for (int i = 0; word[i] != '\0'; i++)
    {
        value += tolower(word[i]);
    }
    return value % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }
    char typeword[LENGTH + 1];

    while (fscanf(file, "%s", typeword) != EOF)
    {
        node *n = malloc(sizeof(node));

        if (n == NULL)
        {
            return false;
        }
        strcpy(n->word, typeword);

        int key = hash(typeword);

        if (table[key] == NULL)
        {
            n->next = NULL;
            table[key] = n;
        }

        else
        {
            n->next = table[key];
            table[key] = n;
        }
        wordCount++;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return wordCount;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        node *noden = table[i];

        while (noden != NULL)
        {
            node *deleteme = noden;
            noden = noden->next;
            free(deleteme);
        }

        table[i] = NULL;
    }
    return true;
}
