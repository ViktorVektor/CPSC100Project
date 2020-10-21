arr = [0] * 10
largest = 0

for x in range(0, len(arr)):
    arr[x] = int(input("Enter a number: "),10)
    if(largest < arr[x]):
        largest = arr[x]

print(largest)

