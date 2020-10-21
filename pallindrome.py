word = input("Enter a word: ")
word = word.lower()

reverse = ""

for x in range(0,len(word)):
    reverse += word[len(word)-x-1]

if(reverse == word):
    print("TRUE")
else:
    print("FALSE")
