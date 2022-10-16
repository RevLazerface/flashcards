import os
import sys
import random
import csv
import string


# TODO Include a create subject function
def main():
    # Begin by initiating the desired subject
    print("\nWelcome to flashcards.py! Before we begin, please pick a subject from the list:\n")
    subject = choose_subject()

    # Upon opening the program, ask if the user wants to take a test or add a new flashcard
    print("\nWhat a delightful choice! What would you like to do now?")
    
    # Set variable to track if any tasks have been completed
    continued = 0
    while True:

        # Only includes this prompt if a task has already been completed
        if continued == 1:
            print("\nTask completed exquisitely! Do you wish to perform another task, or exit the program?")

        # Choose what task is to be performed, returning to this prompt once concluded, or exitting on exit input
        print("\n  - -- Menu -- -\n- Submit 'REVIEW' to review flashcards\n- Submit 'TEST' to take the test\n- Submit 'ADD' to add a flashcard\n- Submit 'CHANGE' to change subjects\n- Submit 'EXIT' to exit the program")
        task = input("\nSubmit: ").strip()
        if task == "REVIEW":
            review_cards(subject)
            continued = 1
            continue
        elif task == "TEST":
            run_test(subject)
            continued = 1
            continue
        elif task == "ADD":
            add_card(subject)
            continued = 1
            continue
        elif task == 'CHANGE':
            subject = choose_subject()
            continue
        elif task == "EXIT":
            sys.exit("\nThat was gorgeous, you're gorgeous, stay gorgeous.\n")
        else:
            print("Invalid input, let's try that again shall we?")
            continued = 0
            continue


def review_cards(subject):
    # Propt user to either review cards individually or all at once
    try:
        with open(subject, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            card_list = list(csv_reader)
    except FileNotFoundError:
        raise FileNotFoundError("Somehow you selected a file that doesn't exist. That shouldn't be possible but you did it. Impressive!")

    while True:
        print("\nWould you like to review cards individually, or print them all at once?\n- Submit 'ONE' to view individual cards\n- Submit 'ALL' to view all cards at once")
        view = input("Submit: ")
        if view == "ONE":
            #TODO
            print("\nPlease submit the index number for the desired card from the following list:")
            counter = 1
            for card in card_list:
                print(f"- {counter} - {string.capwords(card['card_title'])}")
                counter += 1
            pick = val_num_input("Card Number: ", card_list)
            print(the(card_list[pick-1]))
        elif view == "ALL":
            for card in card_list:
                print(f"\n{the(card)}")
        else:
            print("Invalid input, let's try that again shall we?")
            continue
        next = input("Submit 'AGAIN' to continue reviewing, or submit 'RETURN' to return to the top menu: ")
        if next == 'AGAIN':
            continue
        elif next == 'RETURN':
            return


# TODO Error checking
def run_test(subject):
    # Read csv file with flashcard data into a list
    try:
        with open(subject, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            card_list = list(csv_reader)
    except FileNotFoundError:
        raise FileNotFoundError("Somehow you selected a file that doesn't exist. That shouldn't be possible but you did it. Impressive!")

    # Randomize list so that each test is different
    random.shuffle(card_list)

    # Give detailed instructions on how to answer, including multiple correct answers
    print("\nEach multiple choice question will be randomly generated from one of the fields on each card. Simple input the numeral of the correct answer. For questions with multiple correct answers, input each correct answer one at a time.\n")
    
    # Generate a random question for each card, tracking correct answers
    correct = 0
    q_num = 0
    for card in card_list:
        q_num += 1
        print(f"Question {q_num}\n")
        if random_q(card, card_list):
            correct += 1

    # Print results and exit function, no output necessary
    print(f"Results: {correct}/{q_num} correct answers\n")
    return


def add_card(subject):
    while True:
        #Load empty card dict and load full list of dicts into variable
        card = {}
        try:
            with open(subject, mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                keys = csv_reader.fieldnames
        except FileNotFoundError:
            raise FileNotFoundError("Somehow you selected a file that doesn't exist. That shouldn't be possible but you did it. Impressive!")

        # Gather fields directly from the keys list to preserve the correct order
        fields = list(keys)
        fields.remove('card_title')

        # Collect inputs for each field
        # NOTE This is the only section of the program that takes unrestricted user input. If the user wants to not follow instructions and make a dumb card, that's on them!
        print("\nComplete the prompts to add your new flashcard!\nFor fields with multiple values, input all values at once in a list separated by commas (Example: blue, green, red, etc...)\n(WARNING: Any input separated by commas will count each side of the comma as separate entries, use commas with caution!)")
        card["card_title"] = input("Card Title: ").strip().lower()
        retry = False
        for field in fields:
            value = input(f"{string.capwords(field)}: ")
            # ERROR CHECKING FOR INPUT
            if "+++" in value:
                print("I didn't warn you because I didn't think this would come up, but please don't include '+++' in your entry, it jams me up good")
                retry = True
                break
            elif value == "":
                print("Please don't leave any selection blank, input 'none' instead")
                retry = True
                break

            # Handle multi-value entries by storing them all in a single string separated by a "+++"
            values = list(value.split(","))
            entries = []
            for _ in values:
                if _.strip().lower() != "":
                    entries.append(_.strip().lower())
            entry = "+++".join(entries)
            card[field] = entry

        if retry == True:
            print("Let's try that again....\n")
            continue

        # Check with user that all entered data is valid
        print("Would you like to submit the following flashcard?\n")
        print(the(card))
        while True:
            okay = input("Submit? (Y/N): ").strip()

            # Allow user to submit, retry, or exit after reviewing data
            if okay == "Y":
                try:
                    with open(subject, 'a') as csv_file:
                        writer = csv.DictWriter(csv_file, fieldnames=keys)
                        writer.writerow(card)
                except FileNotFoundError:
                    raise FileNotFoundError("Somehow you selected a file that doesn't exist. That shouldn't be possible but you did it. Impressive!")

                return
            elif okay == "N":
                try_again = input("Submit 'AGAIN' to try again or 'RETURN' to go back to the top menu: ")
                if try_again == "AGAIN":
                    break
                elif try_again == "RETURN":
                    return
                else:
                    print("Invalid input. Let's try that one again, shall we?\n")
                    continue
            else:
                print("Invalid input. C'mon now it's just one letter, you can do it!\n")
                continue
        continue


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


def choose_subject():
    # This program requires the relevant .csv files to be stored in a folder within the main directory entitled "subjects"
    
    # Retrieve path to the folder by adding the folder name to the main directory path
    script_dir = os.path.dirname(__file__)
    s = "subjects"
    path = os.path.join(script_dir, s)

    # Get file names from folder and print them one by one, properly formatted
    file_names = os.listdir(path)
    counter = 1
    print("Subjects:\n")
    for file in file_names:
        if file.endswith(".csv"):
            print(f"- {counter} - {string.capwords(file.removesuffix('.csv').replace('_', ' '))}")
            counter += 1

    # Take the numeric input to index the list and generate the file path as a string, then return that string
    choice = val_num_input("\nEnter the corresponding number for your desired subject: ", file_names)
    subject = "/".join([s, file_names[choice - 1]])
    return subject
    

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


def the(card):
# Take the dict and print it out with nicer formatting
    fields = gather_fields(card)
    printable = list(f"-------- ----- --- -- - -\n-- - {string.capwords(card['card_title'])} - --\n")
    for field in fields:
        printable.append(f"- {string.capwords(field)}: {string.capwords(card[field].replace('+++', ', '))}\n")
    printable.append("-------- ----- --- -- - -\n")
    full_card = "".join(printable)
    return full_card


def gather_fields(card):
    # This gathers a list of all fields except the card title
    try:
        fields = list(card.keys())
    except:
        raise ValueError("card.keys() couldn't be listified! Where did I leave those darn things?!")
    fields.remove("card_title")
    return fields


def gather_entries(card, field):
    # This function handles the retrieval and unpacking of any number of +++ separated entries in a column
    var = card[field].split("+++")
    try:
        list_var = list(var)
    except:
        raise ValueError("list_var couldn't be listified! I'm mystified!")
    return list_var








if __name__ == "__main__":
    main()