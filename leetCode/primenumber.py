def isPrime(number):
    isprime = True
    for i in range(2, number):
        if number%i == 0:
            isprime = False
    if isprime:
        print(f"{number} is a prime number")
    else:
        print(f"{number} is not a prime number")
isPrime(12)