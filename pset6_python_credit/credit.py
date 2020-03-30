from cs50 import get_string


def main():
    # Gets the credit card number from the user.
    card_number = get_string("Number: ")

    assert identify_card("378282246310005") == "AMEX"
    assert identify_card("371449635398431") == "AMEX"
    assert identify_card("5555555555554444") == "MASTERCARD"
    assert identify_card("5105105105105100") == "MASTERCARD"
    assert identify_card("4111111111111111") == "VISA"
    assert identify_card("4012888888881881") == "VISA"
    assert identify_card("1234567890") == "INVALID"

    print(identify_card(card_number))


def identify_card(card_number):
    """
    Identifies the type of the card:
        AMEX, VISA, MASTERCARD OR INVALID
    """
    # Stores the length of the card number.
    length = len(str(card_number))

    # Validates that the card number has only digits.
    if (not card_number.isdigit()):
        return "INVALID"

    # Validates the card number length.
    if (length not in [13, 15, 16]):
        return "INVALID"

    # Validates the card number digits.
    if (not validate_card_number(card_number)):
        return "INVALID"

    check_digits = int(card_number[0:2])

    if (check_digits == 34 or check_digits == 37):
        if (length == 15):
            return "AMEX"
    elif (check_digits >= 51 and check_digits <= 55):
        if (length == 13 or length == 16):
            return "MASTERCARD"
    elif (check_digits >= 40 and check_digits <= 49):
        if (length == 16):
            return "VISA"
    else:
        return "INVALID"


def validate_card_number(card_number):
    """
    Validates the card number with Luhn’s Algorithm.
    """
    # Reverse the card number
    card_number = "".join(reversed(card_number))

    # Splits the numbers to even and odds.
    # The ods are multiplied by 2.
    odds = evens = ''
    for counter, digit in enumerate(str(card_number)):
        if counter % 2 == 0:
            evens += str(digit)
        else:
            odds += str(int(digit) * 2)

    # The card number is valid if
    # the sum of the digits sums ends with 0.
    evens_sum = sum_digits(evens)
    odds_sum = sum_digits(odds)
    total = evens_sum + odds_sum
    last_digit = str(total)[-1]
    return last_digit == '0'


def sum_digits(number):
    """
    Sums the digits of a number.
    """
    card_sum = 0
    for d in str(number):
        card_sum += int(d)
    return card_sum


main()
