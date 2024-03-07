import string
def ceasar_cypher(text,shift):
    alphabets = list(string.ascii_lowercase)
    #alphabets.append(' ')
    text_list = list(text)
    new_list = []
    for i in text:
        if i in alphabets:
            i = alphabets[alphabets.index(i) - alphabets.index(alphabets[shift-26])]
            new_list.append(i)
        else:
            new_list.append(' ')
    for i in new_list:
        print(i, end= '')
    

ceasar_cypher('hello world', 25)