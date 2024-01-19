a = {'a' : 123,
     'b' : 23234,
     'c' : 234}
value = {i for i in a if a[i]==23234}
print(value)