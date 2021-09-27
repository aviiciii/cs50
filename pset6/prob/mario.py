from cs50 import get_int

h = 0

# get height
while h < 1 or h > 8:
    h = get_int("Height: ")

# print spaces and hashes
for i in range(h):
    for j in range(h):
        if i + j < h - 1:
            print(" ", end="")
        else:
            print("#", end="")
    print("")
