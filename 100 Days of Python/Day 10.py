#calculator
continued = 'y'
first_number = int(input("What is the first number?"))
while continued == 'y': 
    
    operation = input("Pick an operation")
    second_number = int(input("What is the second number?"))
    if operation == '+':
        final =  first_number+second_number
        print(final)
    elif operation == '-':
        final = first_number-second_number
        print(final)
    elif operation == '/':
        final = first_number/second_number
        print(final)
    elif operation == '*':
        final = first_number*second_number
        print(final)
    continued = input(f"Type 'y' to contnue with {final} or type 'n' to start a new calculation")
    if continued == 'y':
        first_number = final