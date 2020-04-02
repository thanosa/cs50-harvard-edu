import csv

from sys import argv


def main():
    """
    Identifies a person based on their DNA STRs.
    """

    # Validates the number of arguments
    if len(argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        exit(1)

    # Reads the command line arguments.
    database_filename, sequence_filename = argv[1], argv[2]

    # Runs all the tests
    test_all("tests.csv")

    # Identifies the person in the DNA db from the sequence .
    print(identify_person(database_filename, sequence_filename))


def test_all(test_filename):
    """
    Runs all that are specifies in a csv file.
    """

    assert identify_person("databases/small.csv", "sequences/1.txt") == "Bob"
    assert identify_person("databases/small.csv", "sequences/2.txt") == "No match"
    assert identify_person("databases/small.csv", "sequences/3.txt") == "No match"
    assert identify_person("databases/small.csv", "sequences/4.txt") == "Alice"
    assert identify_person("databases/large.csv", "sequences/5.txt") == "Lavender"
    assert identify_person("databases/large.csv", "sequences/6.txt") == "Luna"
    assert identify_person("databases/large.csv", "sequences/7.txt") == "Ron"
    assert identify_person("databases/large.csv", "sequences/8.txt") == "Ginny"
    assert identify_person("databases/large.csv", "sequences/9.txt") == "Draco"
    assert identify_person("databases/large.csv", "sequences/10.txt") == "Albus"
    assert identify_person("databases/large.csv", "sequences/11.txt") == "Hermione"
    assert identify_person("databases/large.csv", "sequences/12.txt") == "Lily"
    assert identify_person("databases/large.csv", "sequences/13.txt") == "No match"
    assert identify_person("databases/large.csv", "sequences/14.txt") == "Severus"
    assert identify_person("databases/large.csv", "sequences/15.txt") == "Sirius"
    assert identify_person("databases/large.csv", "sequences/16.txt") == "No match"
    assert identify_person("databases/large.csv", "sequences/17.txt") == "Harry"
    assert identify_person("databases/large.csv", "sequences/18.txt") == "No match"
    assert identify_person("databases/large.csv", "sequences/19.txt") == "Fred"
    assert identify_person("databases/large.csv", "sequences/20.txt") == "No match"


def identify_person(database_filename, sequence_filename):
    """
    Identifies a person based on their DNA STRs.
    The DNA sequence is parced extracting the maximum occurences
    of particular STRs. Once the parse is done, the person is looked up
    in the database based on the occurencies.
    """

    # Loads the database and sequence csv files into the memory.
    database_fields, database_rows = read_csv(database_filename, True)
    sequence = read_single_line_text_file(sequence_filename)

    # Count the occurencies of each of the str_sequence.
    # The first element is ignored as it is the "name"
    #
    # Every time we find an STR occurence we need to jump
    # by the length of the STR as otherwise we will count
    # multiple time the STRs that have repetitive parts
    # such as: TATATATA which in reality they are two TATA
    # and not 3: TATAXXXX, XXTATAXX and XXXXTATA
    all_matches = []
    for str_sequence in database_fields[1:]:
        max_matches = 0
        matches = 0
        i = 0
        while True:
            token = sequence[i:i + len(str_sequence)]
            if token == str_sequence:
                matches += 1
                if max_matches < matches:
                    max_matches = matches
                i += len(str_sequence)
            else:
                matches = 0
                i += 1
            if i == len(sequence) - len(str_sequence):
                break
        all_matches.append(max_matches)

    # Checks if there is a name with the particular STR matches.
    result = ""
    for database_row in database_rows:
        name = database_row[0]
        if list(map(int, database_row[1:])) == all_matches:
            result = name
            break

    # Returns the result
    return result if result else "No match"


def read_csv(csv_filename, has_header):
    """
    Reads a csv file and returns the header and the rows.
    """

    # Initialization
    fields = []
    rows = []

    # Opens the csv file for read and creates an iterator.
    with open(csv_filename, 'r') as csv_file:
        # Create a csv reader iterator
        csv_reader = csv.reader(csv_file, delimiter=',')

        # Reads the fields from the header of the csv file.
        if has_header:
            fields = csv_reader.__next__()

        # Reads the rest of the rows.
        for row in csv_reader:
            rows.append(row)

    if has_header:
        return fields, rows
    else:
        return rows


def read_single_line_text_file(single_line_filename):
    """
    Reads a text file and returns its single line contents.
    """

    # Opens the file for read.
    with open(single_line_filename, 'r') as single_line_file:
        contents = single_line_file.readlines()

    return contents[0]


main()
