#include <cs50.h>
#include <math.h>
#include <stdio.h>

bool is_card_valid(long card_number, int len);

int main(void)
{
    // Get the card number from the user. 
    long card_number = get_long("Type the credit card number:");
    
    // Checks if the lenth of the card 
    int len = 0;
    
    long test_number = card_number;
    while (test_number > 0)
    {
        test_number = test_number / 10;
        len++;
    }
    
    // Initially checks if the length is fine.
    if (len != 13 && len != 15 && len != 16)
    {
        printf("INVALID\n");
    }
    else
    {
        // Eliminate the check digitst which are the first two.
        int check_digits = card_number / pow(10, (len - 2));
             
        // Check for the AMEX, MASTERCARD, VISA or INVALID card types.
        if ((check_digits == 34 || check_digits == 37) && len == 15 && is_card_valid(card_number, len))
        {
            printf("AMEX\n");
        }
        else if ((check_digits >= 51 && check_digits <= 55) && (len == 13 || len == 16) && is_card_valid(card_number, len))
        {
            printf("MASTERCARD\n");
        }
        else if ((check_digits >= 40 && check_digits <= 49) && len == 16 && is_card_valid(card_number, len))
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
}

bool is_card_valid(long card_number, int len)
{
    // Variable declaration.
    int sum = 0;
    int temp = 0;
    int digit = 0;
    int counter = 1;
    
    // Parses the card number character by character
    while (card_number)
    {
        digit = card_number % 10;
        card_number /= 10;

        if (counter % 2 == 0)
        {
            temp = digit * 2;
        }
        else
        {
            temp = digit * 1;
        }
        
        // Parses the temp sum digit by digit.
        while (temp)
        {
            digit = temp % 10;
            temp /= 10;
            
            sum += digit;
        }

        counter++;
    }
    
    // The last digit should be zero.
    return sum % 10 == 0;
}


