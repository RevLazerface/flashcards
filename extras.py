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


def gather_entries(card, field):
    # This function handles the retrieval and unpacking of any number of @@@ separated entries in a column
    var = card[field].split("@@@")
    try:
        list_var = list(var)
    except:
        raise ValueError("list_var couldn't be listified! I'm mystified!")
    return list_var

def gather_fields(card):
    # This gathers a list of all fields except the card title
    try:
        fields = list(card.keys())
    except:
        raise ValueError(f"{card} couldn't be listified! Where did I leave those darn things?!")
    fields.remove("card_title")
    return fields


def get_list(card, card_list, field):
    # Set an empty list to store all existing values for the relevant key
    full_list = []
    
    for row in card_list:
        entries = gather_entries(row, field)
        full_list.extend(entries)

    # Remove non-unique values from list with set, then turn back to a list because random was weird about set for some reason
    full_list = set(full_list)
    full_list = list(full_list)

    # Gather correct ansnwers and remove them from the list
    correct = gather_entries(card, field)
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


# TODO Create the Subject class and Flashcard subclass*** research subclasses
class Subject:
    def __init__(self, title, card_list, keys):
        self.title = title
        self.card_list = card_list
        self.keys = keys
        self.fields = keys.remove('card_title')

    # TODO Methods: print the card
#NOTE DELETE ONCE Card CLASS IS TESTED
    #def print_card(self, index):
    #    printable = list(f"-------- ----- --- -- - -\n-- - {string.capwords(self.card_list[index]['card_title'])} - --\n")
    #    for field in self.fields:
    #        printable.append(f"- {string.capwords(field)}: {string.capwords(self.card_list[index][field])}\n")
    #    printable.append("-------- ----- --- -- - -\n")
    #    full_card = "".join(printable)
    #    print(full_card)
    
    def __str__(self):
        return self.title


class Card:
    def __init__(self, card):
        self.title = card['card_title']
        self.fields = list(card.keys()).remove('card_title')

    def __str__(self):
        printable = list(f"-------- ----- --- -- - -\n-- - {string.capwords(self.title)} - --\n")
        for field in self.fields:
            printable.append(f"- {string.capwords(field)}: {string.capwords(self[field])}\n")
        printable.append("-------- ----- --- -- - -\n")
        full_card = "".join(printable)
        return full_card