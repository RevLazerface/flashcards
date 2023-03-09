import string, re


class Subject:
    # The subject class stores the relvant info about the currently selected csv file, it's filepath, the list of dicts 
    # for each card, and the dict keys, to make it easily accessible to different parts of the program

    def __init__(self, path, card_list, keys):
        self.path = path
        self.card_list = card_list
        self.keys = keys
        fields = []
        for key in keys:
            if key != 'card_title':
                fields.append(key)
        self.fields = fields
    
    def get_list(self, field):
        # Takes one of the fields, aka csv column names, and gathers a list of every unique entry in all rows.
        full_list = []
        for row in self.card_list:
            c = Card(row)
            entries = c.gather(field)
            full_list.extend(entries)
        full_list = set(full_list)
        return list(full_list)

class Card:
    # The card class stores the relevant info of the currently selected dict, it's fields, title, and the actual 
    # dict object used to initiate the card, varifying that it's properly formatted. It then allows easy gathering of 
    # the entries for each field, and the ability to print the card using my specific graphic formatting.

    def __init__(self, card):
        if not isinstance(card, dict):
            raise Exception("Tried to create a card with an improper input.")
        self.dict = card
        try:
            self.title = card['card_title']
        except KeyError:
            print("The input dict wasn't formatted properly to create a card.")
        fields = []
        for key in list(card.keys()):
            if key != 'card_title':
                fields.append(key)
        self.fields = fields

    def gather(self, field):
        try:
            entry = self.dict[field]
        except KeyError:
            print("The input field wasn't part of the card. How did you do that, seriously?")
        return re.split("~~~", entry)

    def __str__(self):
        printable = list(f"-------- ----- --- -- - -\n-- - {string.capwords(self.title)} - --\n")
        for field in self.fields:
            printable.append(f"- {string.capwords(field)}: {string.capwords(', '.join(self.gather(field)))}\n")
        printable.append("-------- ----- --- -- - -\n")
        full_card = "".join(printable)
        return full_card