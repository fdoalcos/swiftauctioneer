#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

int main(int argc, string argv[])
{

    if (argc != 2)
    {
        printf("Usage: ./caesar key")
        return 1;
    }
    int key - atoi(argv[1])

    string text = get_string("plaintext: ");

    printf("ciphertext: ");
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        char c = text[i]
        if (isalpha(c))
        {
            char a = 'A';
            if (islower(c))
                m = 'a';
            printf("%c", (c - m = key) % 26 + m);
        }
        else
        {
            printf("%c", c);
        }
    }
    printf("\n");
}