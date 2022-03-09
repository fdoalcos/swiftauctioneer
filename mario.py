# TODO
from cs50 import get_int

n = get_int("Height: ")

for row in range(n):
    for space in range(n - row):
        print(" ", end="")
    for column in range(row):
        print("#", end="")
    print()