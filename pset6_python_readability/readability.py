from cs50 import get_string
import re

SENTENCE_CHARS = [".", "!", "?"]
WORD_CHARS = [".", "!", "?", ",", ";", ":", "\""]


def main():

    # Runs all the test
    test_all()

    # Gets the input text from the user.
    text = get_string("Text: ")

    # Calculates the grade and outputs it.
    grade = calc_grade(text, WORD_CHARS, SENTENCE_CHARS)
    print("Grade " + grade)


def test_all():
    """
    Runs all the unit and end to end tests.
    """

    # Unit tests 1.
    text = 'Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, "and what is the use of a book," thought Alice "without pictures or conversation?'
    assert count_letters(text) == 235

    # Unit test 2.
    text = "It was a bright cold day in April, and the clocks were striking thirteen. Winston Smith, his chin nuzzled into his breast in an effort to escape the vile wind, slipped quickly through the glass doors of Victory Mansions, though not quickly enough to prevent a swirl of gritty dust from entering along with him."
    assert count_letters(text) == 250
    assert count_words(text, SENTENCE_CHARS) == 55

    # Unit test 3.
    text = "When he was nearly thirteen, my brother Jem got his arm badly broken at the elbow. When it healed, and Jem's fears of never being able to play football were assuaged, he was seldom self-conscious about his injury. His left arm was somewhat shorter than his right; when he stood or walked, the back of his hand was at right angles to his body, his thumb parallel to his thigh."
    assert count_letters(text) == 295
    assert count_words(text, WORD_CHARS) == 70
    assert count_sentences(text, SENTENCE_CHARS) == 3

    # End to end test 1.
    text = "Congratulations! Today is your day. You're off to Great Places! You're off and away!"
    grade = "Grade 3"
    assert calc_grade(text, WORD_CHARS, SENTENCE_CHARS) == grade

    # End to end test 2.
    text = "Harry Potter was a highly unusual boy in many ways. For one thing, he hated the summer holidays more than any other time of year. For another, he really wanted to do his homework, but was forced to do it in secret, in the dead of the night. And he also happened to be a wizard."
    grade = "Grade 5"
    assert calc_grade(text, WORD_CHARS, SENTENCE_CHARS) == grade

    # End to end test 3.
    text = "As the average number of letters and words per sentence increases, the Coleman-Liau index gives the text a higher reading level. If you were to take this paragraph, for instance, which has longer words and sentences than either of the prior two examples, the formula would give the text an eleventh grade reading level."
    grade = "Grade 11"
    assert calc_grade(text, WORD_CHARS, SENTENCE_CHARS) == grade

    # End to end test 4.
    text = "One fish. Two fish. Red fish. Blue fish"
    grade = "Before Grade 1"
    assert calc_grade(text, WORD_CHARS, SENTENCE_CHARS) == grade

    # End to end test 5
    text = "Would you like them here or there? I would not like them here or there. I would not like them anywhere."
    grade = "Grade 2"
    assert calc_grade(text, WORD_CHARS, SENTENCE_CHARS) == grade

    # End to end test 6.
    text = "Congratulations! Today is your day. You're off to Great Places! You're off and away!"
    grade = "Grade 3"
    assert calc_grade(text, WORD_CHARS, SENTENCE_CHARS) == grade

    # End to end test 7.
    text = "Harry Potter was a highly unusual boy in many ways. For one thing, he hated the summer holidays more than any other time of year. For another, he really wanted to do his homework, but was forced to do it in secret, in the dead of the night. And he also happened to be a wizard."
    grade = "Grade 5"
    assert calc_grade(text, WORD_CHARS, SENTENCE_CHARS) == grade

    # End to end test 8.
    text = "In my younger and more vulnerable years my father gave me some advice that I've been turning over in my mind ever since."
    grade = "Grade 7"
    assert calc_grade(text, WORD_CHARS, SENTENCE_CHARS) == grade

    # End to end test 9.
    text = 'Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, "and what is the use of a book," thought Alice "without pictures or conversation?"'
    grade = "Grade 8"
    assert calc_grade(text, WORD_CHARS, SENTENCE_CHARS) == grade

    # End to end test 10.
    text = "When he was nearly thirteen, my brother Jem got his arm badly broken at the elbow. When it healed, and Jem's fears of never being able to play football were assuaged, he was seldom self-conscious about his injury. His left arm was somewhat shorter than his right; when he stood or walked, the back of his hand was at right angles to his body, his thumb parallel to his thigh."
    grade = "Grade 8"
    assert calc_grade(text, WORD_CHARS, SENTENCE_CHARS) == grade

    # End to end test 11.
    text = "There are more things in Heaven and Earth, Horatio, than are dreamt of in your philosophy."
    grade = "Grade 9"
    assert calc_grade(text, WORD_CHARS, SENTENCE_CHARS) == grade

    # End to end test 12.
    text = "It was a bright cold day in April, and the clocks were striking thirteen. Winston Smith, his chin nuzzled into his breast in an effort to escape the vile wind, slipped quickly through the glass doors of Victory Mansions, though not quickly enough to prevent a swirl of gritty dust from entering along with him."
    grade = "Grade 10"
    assert calc_grade(text, WORD_CHARS, SENTENCE_CHARS) == grade

    # End to end test 13.
    text = "A large class of computational problems involve the determination of properties of graphs, digraphs, integers, arrays of integers, finite families of finite sets, boolean formulas and elements of other countable domains."
    grade = "Grade 16+"
    assert calc_grade(text, WORD_CHARS, SENTENCE_CHARS) == grade


def calc_grade(text, word_chars, sentence_chars):
    """
    computes the approximate grade level needed to comprehend some text
    based on Coleman-Liau formula.
    """

    # Counts the letters within the text.
    letters_count = count_letters(text)

    # Counts the words within the text.
    words_count = count_words(text, word_chars)

    # Counts the sentences within the text.
    sentences_count = count_sentences(text, sentence_chars)

    # Calculates the Coleman-Liau index
    L = (letters_count / words_count) * 100
    S = (sentences_count / words_count) * 100
    index = calc_coleman_liau_index(L, S)

    # Text response based on the index
    if index > 16:
        result = "Grade 16+"
    elif index < 1:
        result = "Before Grade 1"
    else:
        result = f"Grade {index}"
    print(result)
    return result


def count_letters(text):
    """
    Gets a text and counts the letters: a-z A-Z.
    """

    count = 0
    for c in text:
        if c.isalpha():
            count += 1
    return count


def count_words(text, word_chars):
    """
    Gets a text and counts the words
    after replacing the sentence end characters to spaces.
    """

    for c in word_chars:
        text = text.replace(c, " ")
    count = len(text.split())
    return count


def count_sentences(text, sentence_chars):
    """
    Gets a text and counts its sentences based on sentence end characters.
    """

    count = 0
    for c in sentence_chars:
        count += text.count(c)
    return count


def calc_coleman_liau_index(L, S):
    """
    Calculates the Coleman - Liau formula.
    """

    index = round(0.0588 * L - 0.296 * S - 15.8)
    return index


main()

