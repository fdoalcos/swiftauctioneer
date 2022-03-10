from cs50 import get_int

while True:
    n = get_int("Height: ")
    if n > 0 and n < 9:
        break

for row in range(n + 1):
    for space in range(n - row - 1):
        print(" ", end="")
    for column in range(row):
        print("#", end="")
    print()