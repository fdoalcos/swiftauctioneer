# TODO
from cs50 import get_int

from cs50 import get_int

while True:
    n = get_int("Height: ")
    if n > 1 and n < 8:
        break

for row in range(n):
    for space in range(n - row - 1):
        print(" ", end="")
    for column in range(row):
        print("#", end="")
    print()