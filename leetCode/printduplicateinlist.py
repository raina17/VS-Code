def duplicate(a):
    duplicates = []
    for i in a:
        if a.count(i) > 1:
            duplicates.append(i)
    duplicates = set(duplicates)
    duplicates = list(duplicates)
    print(duplicates)

duplicate([10, 20, 30, 20, 20, 30, 40, 50, -20, 60, 60, -20, -20])