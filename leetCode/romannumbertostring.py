symbols = ['I', 'V', 'X', 'L', 'C', 'D', 'M']
end_user = input("Enter the roman numbers")
numeral = 0
for i in end_user:
    if i == 'I':
        numeral +=1
    elif i == 'V':
        numeral += 5
    elif i == 'X':
        numeral +=10
    elif i == 'L':
        numeral += 50
    elif i == 'C':
        numeral += 100
    elif i == 'D':
        numeral += 500
    elif i == 'M':
        numeral += 1000

if 'IV' in end_user or 'IX' in end_user:
    numeral -= 2
if 'XL' in end_user or 'XC' in end_user:
    numeral -= 20
if 'CD' in end_user or 'CM' in end_user:
    numeral -= 200


print(numeral)
