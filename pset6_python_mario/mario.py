# Getting the height from the user that should be positive integer.
while True:
    height = input("Height: ")

    if height.isdigit():
        height = int(height)
        if height >= 1 and height <= 8:
            break

# Prints out the super Mario obstacle.
for i in range(height):
    print(" " * (height - i - 1) + "#" * (i + 1) + "  " + "#" * (i + 1))
