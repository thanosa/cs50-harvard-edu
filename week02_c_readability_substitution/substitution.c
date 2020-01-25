#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

bool check_is_letter(char c);

int main(int argc, string argv[])
{
    // Argument handling

    // The user should give a key
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    // Storing the key in upper case.
    string key = argv[1];

    // Storing the length of the key.
    int key_len = strlen(key);

    // The key should be 26 characters.
    if (strlen(key) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    // Check if key contains only letters.
    // Converts the key to upper case.
    for (int i = 0; i < key_len; i++)
    {
        if (!check_is_letter(key[i]))
        {
            printf("Invalid character: %c\n", key[i]);
            return 1;
        }
        key[i] = toupper(key[i]);
    }

    // Check if all letters are contained within the key.
    // At this stage the key have been converted to upper case.
    bool flag;
    for (int i = 0; i < 26; i++)
    {
        flag = false;
        for (int j = 0; j < key_len; j++)
        {
            if (key[j] == 65 + i)
            {
                flag = true;
            }
        }
        if (flag == false)
        {
            printf("Key doesn't contain all letters\n");
            return 1;
        }
    }

    // Get the plain text from the user.
    string plain_text = get_string("plaintext:");

    // Stores the plain text length.
    int plain_len = strlen(plain_text);

    char plain_char;
    char key_char;
    string cipher_text = plain_text;

    bool is_upper = false;

    int alphabet_index = -1;

    for (int i = 0; i < plain_len; i++)
    {
        // Stores the plain letter to encrypt.
        plain_char = plain_text[i];

        // Check if the character is a letter
        if (check_is_letter(plain_char))
        {
            // Check if the letter is upper case.
            is_upper = isupper(plain_char);

            // Translates the letter to ascii number
            if (is_upper)
            {
                alphabet_index = plain_char - 65;
                cipher_text[i] = toupper(key[alphabet_index]);
            }
            else
            {
                alphabet_index = plain_char - 97;
                cipher_text[i] = tolower(key[alphabet_index]);
            }
        }
        else
        {
            cipher_text[i] = plain_char;
        }
    }

    // Prints out the result and the return code.
    printf("ciphertext:%s", cipher_text);
    printf("\n");
    return 0;
}

bool check_is_letter(char c)
{
    return ((c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z'));
}