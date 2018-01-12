#define _XOPEN_SOURCE
#include <unistd.h>
#include <stdio.h>
#include <cs50.h>
#include <string.h>

void permute(char n[], char arr[], char salt[], char hash[], int r, int position)
{
    
    if (strncmp(crypt(arr, salt), hash, strlen(hash)) == 0)
    {
        printf("%s\n", arr);
        exit(0);
    }
    
    int length = strlen(n);
    if (position == r)
    {
        return;
    }
    
    for (int i = 0; i < length; i++)
    {
        arr[position] = n[i];
        permute(n, arr, salt, hash, r, position + 1);
    }
    
}

int main(int argc, char *argv[])
{
    
    if (argc != 2)
    {
        return 1;
    }
    
    string hash;
    char salt[3];
    hash = argv[argc - 1];
    
    salt[0] = hash[0];
    salt[1] = hash[1];
    
    char alpha[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    for (int r = 1; r < 6; r++)
    {
        char arr[r];
        for (int position = 0; position < r ; position++)
        {
            arr[position] = alpha[0];
        }
        
        permute(alpha, arr, salt, hash, r, 0);
    }

};