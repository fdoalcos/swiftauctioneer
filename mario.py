# TODO
from cs50 import get_int

while True:
    n = get_int("Height: ")
    if n > 0 and n < 9:
        break

for row in range(n):
    for space in range(n - row):
        print("", end="")
    for column in range(row + 1):
        print("#", end="")
    print()