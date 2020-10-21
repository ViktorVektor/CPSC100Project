price = int(input("How much do you need?: "), 10)

ones = price % 5;
fives = (price - ones)/5

print("You would need " + str(fives) + " fives, and " + str(ones) + " ones.")


