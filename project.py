from pathvalidate import sanitize_filename
import os, sys, random, csv, string, re

"""
This program is a terminal based flashcard studying program that allows users review cards, test themselves on the 
card's contents, add new cards, and change or even create entirely new subjects. They can review one card at a time 
or all cards simultaneously, and the test randomly generates multiple choice questions, once for a randomly selected
field on each card. The program requires the relevant .csv files to be stored in a folder within the main directory
entitled "subjects" and each .csv must have one column titled "card_title". The text-based user interface is fairly 
simplistic and rigid, with the user required to input commands exactly as instructed. The cards and subject, however,
are left to the user to input as they see fit with few limitations.
""" 
   
def main():
    """
    Main() initiates the flashcard session and then acts as a main menu from which the user decides which 
    of the program's tasks they want to undertake. All of the tasks return the user to this main 
    menu once completed so that the user can take perform another task or exit.
    """
    
    # Greet user and initiate the desired subject as a Subject object
    print("\nHail and well met! Welcome to flashcards.py! Before we begin, kindly pick a subject from the list:\n")
    s = choose_subject()
    print("\nWhat a delightful choice! What would you like to do now?")
    continued = 0
    while True:
    
        # Only include this prompt if any task has already been completed
        if continued == 1:
            print("\nTask completed exquisitely! Do you wish to perform another task, or exit the program?")

        # Choose what task is to be performed, returning to this prompt once concluded, or exitting on exit input
        print("\n  - -- Menu -- -\n- Submit 'REVIEW' to review flashcards\n- Submit 'TEST' to take the test\n- Submit 'ADD' to add a flashcard\n- Submit 'CHANGE' to change subjects\n- Submit 'CREATE' to create a new subject\n- Submit 'EXIT' to exit the program")
        task = input("\nSubmit: ").strip()

        if task == 'REVIEW':
            while True:
                # Select whether to review one or all cards
                print("\nA wise decision indeed! Would you like to review cards individually, or print them all at once?\n- Submit 'ONE' to view individual cards\n- Submit 'ALL' to view all cards at once")
                view = choose("Submit: ", 'ONE', 'ALL')
                if view == 'ONE':
                    # List the card titles with index numbers to choose from, then print chosen card
                    print("\nPlease submit the index number for the desired card from the following list:")
                    counter = 1
                    for sub_card in s.card_list:
                        print(f"- {counter} - {string.capwords(sub_card['card_title'])}")
                        counter += 1
                    pick = val_num_input("Card Number: ", s.card_list) - 1  
                    rev_card = Card(s.card_list[pick])
                    print(f"\n{rev_card}")
                
                elif view == 'ALL':
                    # Print every card in the list
                    print("")
                    for card in s.card_list:
                        rev_card = Card(card)
                        print(rev_card)   

                # Prompt the user to review another card or return to the main menu
                print("What would you like to do next?")
                next = choose("Submit 'AGAIN' to review again or 'RETURN' to go back to the top menu: ", 'AGAIN', 'RETURN')
                if next == 'AGAIN':
                    continue
                else:
                    break
            continued = 1
            continue

        elif task == 'TEST':       
            # Generate a random question for each card in a random order, tracking correct answers
            print("\n- -- Test Instructions -- -\nWhat a bold selection! In this test you will be presented with a multiple choice question about each card in this subject. Each multiple choice question will be randomly generated from one of the fields on each card. Simply input the numeral of what you believe to be the correct answer. For questions with multiple correct answers, input each correct answer one at a time.\n")
            test_list = s.card_list
            random.shuffle(test_list)
            correct = 0
            q_num = 0
            for _ in test_list:
                q_num += 1
                print(f"Question {q_num}\n")
                if random_q(_, s):
                    correct += 1
            
            # Print results and return to menu
            print(f"Results: {correct}/{q_num} correct answers\n")  
            continued = 1
            continue

        elif task == 'ADD':
            while True:
                # Allow user to generate a new card based on the current subject and review the card before submitting
                print("\nWhat an inspired pick! Complete the prompts to add your new flashcard. For fields with multiple values, input all values at once in a list separated by commas (Example: blue, green, red, etc...)\n\n!! WARNING: Any input separated by commas will count each side of the comma as separate entries, use commas with caution !! Also, please avoid using the '~' symbol, especially at the beginning or end of your entry.\n")
                add_card = create_card(s.fields)
                if not add_card:
                    break
                print("\nWould you like to submit the following flashcard?\n")
                print(add_card)
                add = choose("Sumbit? (Y/N): ", 'Y', 'N')
                # Upon submission, update the .csv and append the new dict to s.card_list manually
                if add == "Y":
                    try:
                        with open(s.path, 'a') as csv_file:
                            writer = csv.DictWriter(csv_file, fieldnames=s.keys)
                            writer.writerow(add_card.dict)
                    except FileNotFoundError:
                        raise FileNotFoundError("Somehow you selected a file that doesn't exist. That shouldn't be possible but you did it. Impressive!")
                    s.card_list.append(add_card.dict)
                    print("\nCard officially laminated and added to the folder. So glossy! What would you like to do now?")
                elif add == "N":
                    print("\nCard officially crumpled up and thrown in the bin. Who needs it?! What would you like to do now?")
                
                # Prompt the user to make another card or return to the main menu
                what_now = choose("Submit 'AGAIN' to try again or 'RETURN' to go back to the top menu: ", 'AGAIN', 'RETURN')
                if what_now == 'AGAIN':
                    continue
                else:
                    break
            continued = 1
            continue

        elif task == 'CHANGE':
            # Choose new subject and update the primary subject object
            print('What a concept! We could all use a little change. Choose from one of the following:')
            s = choose_subject()
            continued = 1
            continue

        elif task == 'CREATE':
            print("\nWow, such an enterprising option! In order to create a brand new subject, you'll just need a subject name, the information fields you want to be tested on, and one full flashcard with whichto start it off. Follow these step by step instructions, and don't worry, you'll get a chance to review everything at the end!")
            while True:
                # Prompt user for subject name, since it will be used as a file name it is first cleaned and validated
                new_subject = input("\nFirst, enter the cool name you picked for the new subject you wish to add\n\nSubject: ")
                if new_subject == "":
                    print("Your subject needs a name! Do you want to retry your subject submission?")
                    retry = choose("Submit 'AGAIN' to try again or 'RETURN' to go back to the top menu: ", 'AGAIN', 'RETURN')
                    if retry == 'AGAIN':
                        continue
                    else:
                        break
                sani_subject = sanitize_filename(new_subject)
                if new_subject != sani_subject:
                    print(f"Cool though it was, your subject name contained some invalid characters that had to be removed. Is this subject name ok?\nNew name: {string.capwords(sani_subject)}")
                    val_sub = choose("Submit? (Y/N): ", 'Y', 'N')
                    if val_sub == 'Y':
                        new_subject = sani_subject
                    else:
                        print("Do you want to retry your subject submission?")
                        retry = choose("Submit 'AGAIN' to try again or 'RETURN' to go back to the top menu: ", 'AGAIN', 'RETURN')
                        if retry == 'AGAIN':
                            continue
                        else:
                            break

                # Prompt user for the new subject's fields and clean them
                new_fields = input("\nNext, input the names of each nifty field you wish the subject to contain in a single list separated by commas (Ex: 'color, shape, size')\n!! WARNING: Any input separated by commas will count each side of the comma as separate entries, use commas with caution !!\n\nFields: ").split(",")
                for _ in range(len(new_fields)):
                    if new_fields[_] == "":
                        new_fields.remove(new_fields[_])
                    else:
                        new_fields[_] = new_fields[_].strip()
                if new_fields == [] or new_fields == "":
                    print("Your subject needs fields! Do you want to retry your subject submission?")
                    retry = choose("Submit 'AGAIN' to try again or 'RETURN' to go back to the top menu: ", 'AGAIN', 'RETURN')
                    if retry == 'AGAIN':
                        continue
                    else:
                        break

                # Prompt user to generate a card with the new fields then check with user that all entered data is valid
                print("\nAlready amazing, and just one more step to go! Finally, fill out your new subject's first flashcard. Once again, for multiple entries in one field, separate each entry with a comma\n")
                new_card = create_card(new_fields)
                print("\nWould you like to initiate your new subject using the following flashcard? Once you have it will be availble to select from the list of subjects by typing 'CHANGE' into the main menu.\n")
                print(f"- -- {string.capwords(new_subject)} -- -\n")
                print(new_card)
                okay = choose("\nCreate Subject? (Y/N): ", 'Y', 'N').strip()

                # After reviewing data, allow user to submit the new subject, retry, or exit
                if okay == "Y":
                    fieldnames = ["card_title"]
                    fieldnames.extend(new_fields)
                    with open(f"subjects/{new_subject.replace(' ', '_').lower()}.csv", 'w') as csv_file:
                        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerow(new_card.dict)
                        print("\nAbsolutely astounding! This amazing new subject can now be choose from the available list of subjects using the 'CHANGE' task in the main menu.")
                    break
                elif okay == "N":
                    try_again = choose("Submit 'AGAIN' to try again or 'RETURN' to go back to the top menu: ", 'AGAIN', 'RETURN')
                    if try_again == "AGAIN":
                        continue
                    else:
                        break
            continued = 1
            continue

        elif task == 'EXIT':
            sys.exit("\nThat was gorgeous, you're gorgeous, stay gorgeous.\n")
        else:
            print("Invalid input, let's try that again shall we?")
            continued = 0
            continue

def random_q(card, subject):
    """
    Random_q creates a randomly generated question for a given card, returning True for a correct answer and False 
    for and incorrect answer
    """

    # Set the title and fields as variables and pick a random field to generate a question from
    q_card = Card(card)
    q = random.randint(0, len(subject.fields)-1)
    field = subject.fields[q]

    # Using the list of all possible answer and the list of correct answers, generate multiple choice options with at most 3 wrong answers
    full_list = subject.get_list(field)
    correct = q_card.gather(field)
    for item in correct:
        full_list.remove(item)
    if len(full_list) < 3:
        options = random.sample(full_list, k=len(full_list))
    else:
        options = random.sample(full_list, k=3)
    options.extend(correct)
    random.shuffle(options)

    # Obtain the multiple choice options and generate the question, adjusting for single or multiple correct options
    print(f"- -- Card: {string.capwords(q_card.title)} -- -")
    if len(correct) == 1:
        print(f"Which of these {field} options is correct?")
    elif len(correct) > 1:
        print(f"Which {len(correct)} of these '{field}' options are correct?")
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
                print(q_card)
        else:
            print("\nIncorrect! Here's the real info:")
            print(q_card)
            return False
    return True

def choose_subject():
    """
    Choose_subject presents a list of all .csv files located in the "subjects" folder and allows the user to 
    select one, returning the path to said file as well as the list of dictionaries and the column names which 
    are then fed into main's other functions 
    """
    
    # Retrieve path to the folder by adding the folder name to the main directory path
    script_dir = os.path.dirname(__file__)
    path = os.path.join(script_dir, "subjects")

    # Get file names from folder and print them one by one, properly formatted, with index numbers
    file_names = os.listdir(path)
    sub_list = get_subjects(file_names)
    counter = 1
    for sub in sub_list:
        print(f"- {counter} - {sub}")
        counter += 1

    # Read the selected .csv, checking for proper formatting, and use the data to initiate and return a Subject object 
    choice = val_num_input("\nEnter the corresponding number for your desired subject: ", file_names) - 1
    subject = "/".join(["subjects", file_names[choice]])
    try:
        with open(subject, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            card_list = list(csv_reader)
            keys = csv_reader.fieldnames
    except FileNotFoundError:
        raise FileNotFoundError("Somehow you selected a file that doesn't exist. That shouldn't be possible but you did it. Impressive!")
    if 'card_title' not in keys:
        raise Exception("CSV File not properly formatted - Missing 'card_title'")
    if card_list == []:
        raise Exception("CSV File is empty - no cards!")

    return Subject(subject, card_list, keys)

def create_card(fields):
    """
    Create_card takes a subject's fields and generates an input prompt for each one, checking for valid formating 
    and returning a Card object
    """
    
    counter = 0
    while True:
        # Create and empty dict and begin setting variables
        card = {}
        card["card_title"] = input("Card Title: ").strip().lower()
        retry = False
        
        for field in fields:
            # Fields are invalid if the are empty, begin or end with a ~ symbol, or contain three ~'s in a row`
            if field != "":
                value = input(f"{string.capwords(field)}: ")
            else:
                raise Exception("The field name was empty, which shouldn't be possible but here we are!")
            if re.search("^~", value) or re.search("~$", value):
                print("Please don't begin or end your entry with the '~' character, it jams me up good")
                retry = True
                break
            if re.search("~~~", value):
                print("Please don't include '~~~' in your entry, it jams me up good")
                retry = True
                counter += 1
                break
            elif value == "":
                print("Please don't leave any selection blank, you can just input 'none' instead good buddy!")
                retry = True
                counter += 1
                break

            # Handle multiple values by converting to my formatting if necessary then stores the entry
            entry = set_entry(value)
            card[field] = entry
        
        # If field input is invalid, automatically reprompts
        if retry == True:
            if counter == 3:
                backout = choose("\nThat's three retries, would you like to back out of adding a new card? (Y/N): ", 'Y', 'N')
                if backout == 'Y':
                    return False
                else:
                    counter = 0
                    continue
            else:
                print("Let's try that again....\n")
                continue
        return Card(card)

def val_num_input(string, options):
    """
    val_num_input() prompts the user to input the numeric index of a list of options, then validates that the input
    is an integer within the range, returning the integer to be used to index the actual list.
    """

    tries = 0
    while True:
        if tries == 3:
            print("Warning! One more improper input and the program will exit. I believe in you!")
        if tries == 4:
            raise UserShenanigans
        if options == [] or type(options) != list:
            raise Exception("Well that's just not possible. Either you're screwing around, or I've made a terrible mistake.")
        try:
            answer = float(input(string).strip())
        except ValueError:
            print("Ok that wasn't even a proper number, are you really trying? Here's a hint, it's one of these->123456789")
            tries += 1
            continue
        if answer % 1 != 0:
            print("A fraction? Seriously? Now you're just being silly.")
            tries += 1
            continue
        if not 1 <= answer <= len(options):
            print("That number wasn't in the range of numbers and I think you know it!")
            tries += 1
            continue
        return int(answer)

def choose(prompt, arg1, arg2):
    """
    Choose automates asking a prompt in a while loop to allow reprompting, returning only one of the correct options
    It can't be broken except by input one of the correct options 
    """

    tries = 0
    while True:
        if tries == 3:
            print("Warning! One more improper input and the program will exit. I believe in you!")
        if tries == 4:
            raise UserShenanigans
        choice = input(prompt).strip()
        if choice not in [arg1, arg2]:
            print("\nInvalid input. Please only input one of the stated options exactly as written (case sensitively!)\n")
            tries += 1
            continue
        else:
            break
    if choice == arg1:
        return arg1
    else:
        return arg2

def set_entry(value):
    values = list(value.split(","))
    entries = []
    for _ in values:
        if _.strip().lower() != "":
            entries.append(_.strip().lower())
    entry = "~~~".join(entries)
    return entry

def get_subjects(file_names):
    sub_list = []
    for file in file_names:
        if file.endswith(".csv"):
            sub = string.capwords(file.removesuffix('.csv').replace('_', ' '))
            sub_list.append(sub)
    return sub_list

class UserShenanigans(Exception):
    '''
    Custom class made for exceptions that should realistically be out of the users control to create through the scripts basic 
    functionality. Recieving this error should only be possible by messing with the code directly.
    ''' 

    def __init__(self):
        self.message = "Program exitted due to excessive silliness(you know what you did). It's been a pleasure nonetheless!"
    def __str__(self):
        return self.message        

class Subject:
    """
    The subject class stores the relvant info about the currently selected csv file, it's filepath, the list of dicts 
    for each card, and the dict keys, to make it easily accessible to different parts of the program
    """

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
    re

class Card:
    """
    The card class stores the relevant info of the currently selected dict, it's fields, title, and the actual 
    dict object used to initiate the card, varifying that it's properly formatted. It then allows easy gathering of 
    the entries for each field, and the ability to print the card using my specific graphic formatting.
    """

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

if __name__ == "__main__":
    main()