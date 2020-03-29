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
const unsigned int TABLE_SIZE = 32768;

// Hash table
node *table[TABLE_SIZE];

int nodesCount = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    char lower[LENGTH + 1];

    // convert the word of the text to lower case.
    // we ommit the +1 from the LENGTH as it exists only for the /0.
    int len = strlen(word);
    for (int i = 0; i < len; i++)
    {
        lower[i] = tolower(word[i]);
    }
    lower[len] = '\0';

    // Calculate the hash for the word.
    int hashIndex = hash(lower);

    if (table[hashIndex] == NULL)
    {
        return false;
    }

    // Temporary node
    node *tempNode = table[hashIndex];

    // Trasverses the linked list to find if there is the word in it.
    while (tempNode != NULL)
    {
        if (strcasecmp(word, tempNode->word) == 0)
        {
            return true;
        }
        tempNode = tempNode->next;
    }
    return false;
}

// Hashes word to a number
// Taken from: https://www.cs.yale.edu
unsigned int hash(const char *word)
{
    const unsigned long m = 12;
    const int base = 256;

    unsigned long h;
    unsigned const char *us;

    /* cast s to unsigned const char * */
    /* this ensures that elements of s will be treated as having values >= 0 */
    us = (unsigned const char *) word;

    h = 0;
    while (*us != '\0')
    {
        h = (h * base + *us) % m;
        us++;
    }

    // We need to cap the hash value to the
    return h % TABLE_SIZE;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Open the directory file
    FILE *dictFile;
    dictFile = fopen(dictionary, "r");
    if (dictFile == NULL)
    {
        unload();
        return false;
    }

    char newWord[LENGTH + 1];
    while (fscanf(dictFile, "%s\n", newWord) != EOF)
    {
        // Create the new node.
        node *wordNode = malloc(sizeof(node));
        if (wordNode == NULL)
        {
            unload();
            return false;
        }
        strcpy(wordNode->word, newWord);

        // Calculate the hash for the word.
        int hashIndex = hash(wordNode->word);

        // Add the word to the hash index of the table.
        wordNode->next = table[hashIndex];
        table[hashIndex] = wordNode;

        // Counts the number of the nodes.
        nodesCount++;
    }

    // Close the dictionary file.
    fclose(dictFile);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return nodesCount;
}


// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < TABLE_SIZE; i++)
    {
        // Temporary node used to trasverse the linked list.
        node *tmpNode = table[i];

        // Moves from node to node.
        while (tmpNode != NULL)
        {
            node *nextNode = tmpNode;
            tmpNode = tmpNode->next;
            free(nextNode);
        }
    }

    return true;
}
