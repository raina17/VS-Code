strs = ["flower","flow","flight"]


for i in range(len(strs)):
    first_element = strs[0]   
    if first_element in strs:
        print(first_element)
        print('ok')
        first_element = strs[0]
        strs.pop(0)
    else:
        first_element = first_element[:(len(first_element)-1)]
        print(first_element)
        print('nok')
print(first_element)