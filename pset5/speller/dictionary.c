// Implements a dictionary's functionality
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>

#include "dictionary.h"

typedef struct node
{
    char *word;
    struct node *next;
}
node;

//Global variables
node *head;
bool loaded = false;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // Convert word to lower case
    char str[strlen(word) + 1];
    for (int i = 0; i < strlen(word); i++)
    {
        str[i] = tolower(word[i]);
    }
    str[strlen(word)] = '\0';
    node *cursor = head;
    // Find word in dictionary
    while (cursor)
    {
        if (strcmp(cursor->word, str) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r");
    if (!file)
    {
        return false;
    }
    char word[64];
    head = NULL;
    // Create linked list
    while (fscanf(file, "%s", word) != EOF)
    {
        node *temp = malloc(sizeof(node));
        temp->word = malloc(strlen(word) + 1);
        temp->word[strlen(word)] = '\0';
        if (!temp)
        {
            return false;
        }
        strcpy(temp->word, word);
        temp->next = head;
        head = temp;
    }
    fclose(file);
    loaded = true;
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    if (!loaded)
    {
        return 0;
    }
    node *cursor = head;
    int i = 0;
    while (cursor)
    {
        cursor = cursor->next;
        i++;
    }
    return i;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    node *cursor = head;
    while (cursor)
    {
        node *temp = cursor;
        cursor = cursor->next;
        // Free memory allocated for word;
        free(temp->word);
        // Free memory allocated for the struct;
        free(temp);
    }
    return true;
}
