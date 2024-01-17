symbols_and_values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
end_user = input("Enter the roman numbers")
numeral = 0
if 'IV' in end_user:
    numeral += 4
elif 'VI' in end_user:
    numeral +=6 #'asd'

    '''if i == 'V':
        numeral += 5
    if i == 'X':
        numeral += 10
    if i == 'L':
        numeral += 50
    if i == 'C':
        numeral += 100
    if i == 'D':
        numeral += 500
    if i == 'M':
        numeral += 1000'''
print(numeral)