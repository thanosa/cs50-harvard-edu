#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Getting the tiers from the users constraing from 1 to 8.
    int tiers;
    do 
    {
        tiers = get_int("How many tiers?\n");
    } 
    while (tiers < 1 || tiers > 8);
    
    for (int i = 0; i < tiers; i++)
    {
        // Builds the right part.
        for (int j = 0; j < tiers; j++)
        {
            if (j >= tiers - i - 1)
            {
                printf("#");
            }
            else
            {
                printf(" ");
            }
        }
        
        // Builds the gap in the middle.
        printf("  ");
        
        // Builds the right part.
        for (int j = 0; j < tiers; j++)
        {
            if (j <= i)
            {
                printf("#");
            }
        }
        
        // Adds new row.
        printf("\n");
    }
}
