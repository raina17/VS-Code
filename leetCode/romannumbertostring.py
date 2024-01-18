symbols = ['I', 'V', 'X', 'L', 'C', 'D', 'M']
end_user = input("Enter the roman numbers")
numeral = 0
for i in end_user:
    if i == 'I':
        if end_user.index(i) < end_user.index('V'):
            numeral -= 1
        else:
            numeral +=1
    elif i == 'V':
        numeral += 5
    elif i == 'X':
        if end_user.index(i) > end_user.index('I'):
            numeral += 9
        else:
            numeral +=10
    elif i == 'L':
        numeral += 50
    elif i == 'C':
        numeral += 100
    elif i == 'D':
        numeral += 500
    elif i == 'M':
        numeral += 1000
print(numeral)
