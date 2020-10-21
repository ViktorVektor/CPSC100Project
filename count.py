text = ""
output = ""

#prints out 1 - 100 in a straight line
#
#for x in range(1,101):
#	text = str(x)	
#	output = output + " " + text

print(output)

for x in range(1, 101):
        if(x % 3 == 0):
                print("Fizz")
        elif(x % 5 == 0):
                print("Buzz")
        else:
                print(x)
