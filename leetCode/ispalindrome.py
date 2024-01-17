#isPallindrome

def isPallindrome(numbers):
    if str(numbers) == str(numbers)[::-1]:
        print('Is palindrome')
    else:
        print('Is not palindrome')    

isPallindrome(131)
