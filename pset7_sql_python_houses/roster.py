from sys import argv
from cs50 import SQL


def main():
    """
    Prints a list of students for a given house in alphabetical order
    """
    # Validate the number of arguments.
    if (len(argv) != 2):
        print("Wrong number of arguments")
        exit(1)

    # Stores the command line argument.
    house = argv[1]

    # Create a connection to sqlite3 database.
    db = SQL("sqlite:///students.db")

    # Queries the SQL database to retrieve the student details for a particular house.
    students = db.execute("SELECT first, middle, last, birth FROM students WHERE house = ? ORDER BY last, first", house)

    for student in students:
        # Builds up the name, considering that the middle name can be NULL.
        if student["middle"] != None:
            name = " ".join([student["first"], student["middle"], student["last"]])
        else:
            name = " ".join([student["first"], student["last"]])
        print(f'{name}, born {student["birth"]}')


main()
