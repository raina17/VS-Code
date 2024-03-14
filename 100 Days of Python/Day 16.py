from prettytable import PrettyTable

table = PrettyTable()
table.add_column(['Pokemon', 'Type'])
table.add_rows('Pikachu')
print(table)