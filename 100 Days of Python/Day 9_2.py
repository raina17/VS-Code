names = {}
bids = []
print("welcome t0 secret auction program")
next = 'Yes'
while next == 'Yes':
    name = input("What is your name")
    bid = input("What is your bid?")
    names[name] = bid
    next = input("Are there any other bidders?")
print(names)
for i in names:
    bids.append(int(names[i]))
print(bids)
max_bid = max(bids)
value = [i for i in names if names[i]==str(max_bid)]
print(value)
print(f'The winner is {value[0]} with a bid of {max_bid}')