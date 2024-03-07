def validparenthesis(s):
    open = ['(','{','[']
    pairs = {'(' : ')',
             '[' : ']',
             '{' : '}'}
    empty = 0
    for i in s:
        if i in open:
            #print(pairs[i])
            #print(text[1])
            if pairs[i] == s[(s.index(i)+1)]:
                empty+=1
    if empty == len(s)/2:
        print('fuckyeah')
    else:
        print('naah')
    


validparenthesis("[{}()]")

