#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    // Gets the text from the user.
    string text = get_string("Text: ");

    // Counts the number of:
    //   1. letters
    //   2. spaces
    //   3. specials as { . ! ? }
    int letters = 0;
    int spaces = 0;
    int specials = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == ' ')
        {
            spaces++;
        }

        if ((text[i] >= 'a' && text[i] <= 'z') || (text[i] >= 'A' && text[i] <= 'Z'))
        {
            letters++;
        }

        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            specials++;
        }
    }

    // The number of words is equal to the number of spaces
    // plus 1 for the last.
    int words = spaces + 1;

    // The number of sentences is equal to the number
    // of the special characters . ! and ?
    int sentences = specials;

    // Calculates the average number of letters per 100 words in the text
    float L = ((float) letters / (float) words) * 100;

    // Calculates the average number of sentences per 100 words in the text.
    float S = ((float) sentences / (float) words) * 100;

    // Calculate the index according to Coleman-Liau formula.
    int index = round(0.0588 * L - 0.296 * S - 15.8);

    // Post processes the index so that it can't be
    // less than 1 or more than 16.
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}