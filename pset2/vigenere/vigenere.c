#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int getShift (char c)
{
    if (isupper(c))
    {
        return c - 65;
    }
    else
    {
        return c - 97;
    }
}

char shiftChar(int shift, char c)
{
    if (isupper(c))
    {
        if (c + shift <= 90)
        {
            return c + shift;
        }
        else
        {
            return c + shift - 90 + 65 - 1;
        }
    }
    else
    {
        if (c + shift <= 122)
        {
            return c + shift;
        }
        else
        {
            return c + shift - 122 + 97 - 1;
        }
    }
}

int main(int argc, string argv[])
{

    string plaintext, key;
    int i, j;
    i = 0;
    j = 0;
    key = argv[argc - 1];
    if (argc != 2)
    {
        return 1;
    }
    for (int k = 0; k < strlen(key); k++)
    {
        if (!isalpha(key[k]))
        {
            return 1;
        }
    }
    printf("plaintext: ");
    plaintext = get_string();
    printf("ciphertext: ");
    while (i < strlen(plaintext))
    {
        if (isalpha(plaintext[i]))
        {
            int shift = getShift(key[j % strlen(key)]);
            printf("%c", shiftChar(shift, plaintext[i]));
            i++;
            j++;
        }
        else
        {
            if (plaintext[i] == ' ')
            {
                printf(" ");
            }
            else
            {
                printf("%c", plaintext[i]);
            }
            i++;
        }
    }
    printf("\n");

    return 0;
}