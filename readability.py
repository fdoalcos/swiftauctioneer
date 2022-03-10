# TODO
from cs50 import get_string

text = get_string("Text: ")
words = letters = sentences = i = 0
length = len(text)

# counting letters
if text[i].isalpha():
    letters += 1

# counting words
if (i == 0 and text[i] != " ") or (i != length and text[i] == " " and text[i + 1] != " "):
    words += 1

#counting letters
if text[i] == "." or text[i] == "?" or text[i] == "," or text[i] == "!":
    sentences += 1

L = (letters / words) * 100
S = (sentences / words) * 100

index = round(0.0588 * L - 0.296 * S -15.8)

if index > 16:
    print("Grade 16+")
elif index < 1:
    print("Before grade 1")
else:
    print(f"Grade {index}")

