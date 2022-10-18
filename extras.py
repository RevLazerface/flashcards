import string
import random

def convert_split(value):
    values = list(value.split(","))
    entries = []
    for _ in values:
        if _.strip().lower() != "":
            entries.append(_.strip().lower())
    entry = "@@@".join(entries)
    return entry

def create_card(fields):
    while True:
        card = {}
        card["card_title"] = input("Card Title: ").strip().lower()
        retry = False
        for field in fields:
            value = input(f"{string.capwords(field)}: ")
            # ERROR CHECKING FOR INPUT
            if "@" in value:
                print("Please don't include '@' character in your entry, it jams me up good")
                retry = True
                break
            elif value == "":
                print("Please don't leave any selection blank, input 'none' instead")
                retry = True
                break

            # Handle multi-value entries by storing them all in a single string separated by a "@@@"
            # NOTE I want to make this it's own function to use in create_subjects as well
            entry = convert_split(value)
            card[field] = entry

        if retry == True:
            print("Let's try that again....\n")
            continue
        return card

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
        raise ValueError("card.keys() couldn't be listified! Where did I leave those darn things?!")
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
def random_q(card, card_list):
    # Set the title and fields as variables
    title = card["card_title"]
    fields = gather_fields(card)

    # Pick a random field to generate a question from
    q = random.randint(0, len(fields)-1)
    field = fields[q]

    # Obtain the multiple choice options and generate the question, adjusting for single or multiple correct options
    options, correct = get_list(card, card_list, field)
    print(f"- -- Card: {string.capwords(title)} -- -")
    if len(correct) == 1:
        print(f"Which of these {field} options is correct?")
    elif len(correct) > 1:
        print(f"Which {len(correct)} of these {field} options are correct?")
    for i in range(len(options)):
        print(f"{i+1}. {string.capwords(options[i])}")
    
    # Ask for input once for each correct answer by removing correct answers from the list of correct answers until none remain
    while correct != []:
        answer = val_num_input("Answer: ", options)
        if options[answer-1] in correct:
            correct.remove(options[answer-1])
            if len(correct) > 0:
                print(f"\nCorrect! {len(correct)} more to go....")
            else:
                print("\nCorrect! Here's the full card:")
                print(the(card))
        else:
            print("\nIncorrect! Here's the real info:")
            print(the(card))
            return False
    return True


def the(card):
# Take the dict and print it out with nicer formatting
    fields = gather_fields(card)
    printable = list(f"-------- ----- --- -- - -\n-- - {string.capwords(card['card_title'])} - --\n")
    for field in fields:
        printable.append(f"- {string.capwords(field)}: {string.capwords(card[field].replace('@@@', ', '))}\n")
    printable.append("-------- ----- --- -- - -\n")
    full_card = "".join(printable)
    return full_card


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