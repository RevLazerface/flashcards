import csv

with open("subjects/cocktails.csv", mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    card_list = list(csv_reader)
    keys = csv_reader.fieldnames

print(type(card_list))
print(type(card_list[0]))