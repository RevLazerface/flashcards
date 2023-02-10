import string
import random

#TODO ADD FUNCTION DESCRIPTION COMMENTS, CHECK GIVEN INSTRUCTIONS ARE THOROUGH, ADD ERROR CHECKING

def convert_split(value):
    # Convert_split() takes the user's input and for multi-entry inputs, reformats the string to my specifications

    # Split multi-entry inputs, remove whitespace and set to lowercase
    values = list(value.split(","))
    entries = []
    for _ in values:
        #Check for empty spaces betwen extraneous commas
        if _.strip().lower() != "":
            entries.append(_.strip().lower())
   
    # Single entry inputs will be returned as is, multi-entry inputs will be reformatted with @@@ separators
    entry = "@@@".join(entries)
    return entry


def get_list(card, subject, field):
    # Set an empty list to store all existing values for the relevant key
    full_list = []
#NOTE TURN THIS INTO SUBJECT CLASS METHOD
    for row in subject.card_list:
        c = Card(row)
        entries = c.gather(field)
        full_list.extend(entries)

    # Remove non-unique values from list with set, then turn back to a list because random was weird about set for some reason
    full_list = set(full_list)
    full_list = list(full_list)

    # Gather correct ansnwers and remove them from the list
    correct = card.gather(field)
    for item in correct:
        full_list.remove(item)

    # Make a new list of at most 3 randomly selected incorrect entries
    if len(full_list) < 3:
        options = random.sample(full_list, k=len(full_list))
    else:
        options = random.sample(full_list, k=3)
    options.extend(correct)
    random.shuffle(options)
    return options, correct

    # TODO Error checking


def val_num_input(string, list):
    while True:
        try:
            answer = float(input(string).strip())
        except ValueError:
            print("Ok that wasn't even one number, are you really trying?")
            continue
        if answer % 1 != 0:
            print("A fraction? Seriously? Now you're just being silly.")
            continue
        if not 1 <= answer <= len(list):
            print("That number wasn't in the range and I think you know it!")
            continue
        return int(answer)


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


class Card:
    def __init__(self, card):
        self.card = card
        self.title = card['card_title']
        fields = []
        for key in list(card.keys()):
            if key != 'card_title':
                fields.append(key)
        self.fields = fields

    def gather(self, field):
        var = self.card[field].split("@@@")
        try:
            list_var = list(var)
        except:
            raise ValueError("list_var couldn't be listified! I'm mystified!")
        return list_var

    def __str__(self):
        printable = list(f"-------- ----- --- -- - -\n-- - {string.capwords(self.title)} - --\n")
        for field in self.fields:
            printable.append(f"- {string.capwords(field)}: {string.capwords(', '.join(self.gather(field)))}\n")
        printable.append("-------- ----- --- -- - -\n")
        full_card = "".join(printable)
        return full_card