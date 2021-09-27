from cs50 import get_float

# get change owed
while True:
    cash = get_float("Change owed: ")
    if cash > 0:
        break

# change to pennies
penny = round(cash * 100)

# greedy algorithm

coins = 0

# quater
while penny >= 25:
    penny -= 25
    coins += 1

# dime
while penny >= 10:
    penny -= 10
    coins += 1

# nickel
while penny >= 5:
    penny -= 5
    coins += 1

# penny
while penny >= 1:
    penny -= 1
    coins += 1

print(coins)