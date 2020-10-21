num = int(input("Enter a number: "), 10)

for x in range(2, num+1):
    if(num % x == 0):
        break

print(x)

    
