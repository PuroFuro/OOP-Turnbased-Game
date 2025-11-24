import csv
with open(f'./shop/charms.csv', mode='r') as char_file:
    shop = csv.reader(char_file, skipinitialspace=True)
    next(shop)
    for things in shop:
        if things[1] == "item":
            print((f'{things[0]}: {things[3]} {things[5]}'))