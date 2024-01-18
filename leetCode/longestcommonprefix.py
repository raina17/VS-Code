strs = ["c","acc","ccc"]
first_element = strs[0]
strs.pop(0)
count = 0
if len(strs) > 1:
    
    while count < len(strs)+1:
        
        for i in strs:
            if first_element in i:
                count +=1
            else:
                first_element = first_element[:len(first_element)-1]
    print(first_element)
else:
    print(strs[0])
