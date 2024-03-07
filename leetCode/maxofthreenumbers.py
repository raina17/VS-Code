#multiply all numbers in a list

def multnumbers(numbers):
    first_num = numbers[0]
    for num in range(1, len(numbers)):
        first_num = first_num * numbers[num]
    return first_num

a = multnumbers([1,2,3,2,1,2,2])
print(a)


        