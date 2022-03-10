# TODO
from cs50 import get_float
import sys

coins = 0

while True:
    n = get_float("Owed: ")
    if n > 0:
        break

change = round(int(n * 100))

while change > 0:
    while change >= 25:
        coins += 1
        change -= 25
    while change >= 10:
        coins += 1
        change -= 10
    while change >= 5:
        coins += 1
        change -= 5
    while change >= 1:
        coins += 1
        change -= 1

print(f"{coins}")


