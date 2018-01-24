#include <stdio.h>
#include <cs50.h>

int main (void)
{
    int height = get_int("Height: ");
    while (height < 0 || height > 23)
    {
        height = get_int("Height: ");
    };
    for (int i = 0; i < height; i++)
    {
        for (int j = height; j > 0; j--)
        {
            if (i + 1 > j - 1)
            {
                printf("#");
            }
            else
            {
                printf(" ");
            }
        }
        printf("  ");
        for (int j = 0; j < i + 1; j++)
        {
            printf("#");
        }
        printf("\n");
    };
};