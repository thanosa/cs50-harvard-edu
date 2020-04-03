import csv
from sys import argv
from cs50 import SQL


def main():
    """
    Imports a csv with file into the sqlite3 database.
    The name of each character is split into first middle and last.
    Middle name might be null.
    """
    # Validate the number of arguments.
    if (len(argv) != 2):
        print("Wrong number of arguments")
        exit(1)

    # Stores the command line argument.
    characters_csv_filename = argv[1]

    # Loads the csv file into the memory.
    fields, rows = read_csv(characters_csv_filename, True)

    # Create a connection to sqlite3 database.
    db = SQL("sqlite:///students.db")

    for row in rows:
        # Reads the data from the csv row.
        full_name, house, birth = row

        # Parses the name to identify if there is a middle name.
        full_name_array = full_name.split()
        if len(full_name_array) == 2:
            first, last = full_name_array

            # Stores the data into the sqlite3 database using the existing schema.
            db.execute("INSERT INTO students (first, last, house, birth) VALUES (?, ?, ?, ?)", first, last, house, birth)
        else:
            first, middle, last = full_name_array

            # Stores the data into the sqlite3 database using the existing schema.
            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES (?, ?, ?, ?, ?)", first, middle, last, house, birth)


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


main()
