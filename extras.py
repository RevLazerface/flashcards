import string


class Subject:
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
        # Set an empty list to store all existing values for the relevant key, using set() to remove duplicates
        full_list = []
        for row in self.card_list:
            c = Card(row)
            entries = c.gather(field)
            full_list.extend(entries)
        full_list = set(full_list)
        return list(full_list)

#TODO Prevent anything but a properly formatted dict to be used to initiate a Card within the class itself
class Card:
    def __init__(self, card):
        self.dict = card
        self.title = card['card_title']
        fields = []
        for key in list(card.keys()):
            if key != 'card_title':
                fields.append(key)
        self.fields = fields

    def gather(self, field):
        var = self.dict[field].split("@@@")
        try:
            list_var = list(var)
        except:
            raise ValueError("var couldn't be listified! I'm mystified!")
        return list_var

    def __str__(self):
        printable = list(f"-------- ----- --- -- - -\n-- - {string.capwords(self.title)} - --\n")
        for field in self.fields:
            printable.append(f"- {string.capwords(field)}: {string.capwords(', '.join(self.gather(field)))}\n")
        printable.append("-------- ----- --- -- - -\n")
        full_card = "".join(printable)
        return full_card