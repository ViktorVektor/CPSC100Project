factors = 0

for x in range(1, 101):
    for y in range(1, x+1):
        if(x % y == 0):
            if(y != 1 or y != x):
                break
            else:
                print(y)

                
