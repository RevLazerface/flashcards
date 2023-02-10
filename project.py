from extras import convert_split, get_list, val_num_input, Subject, Card
from pathvalidate import sanitize_filename
import os
import sys
import random
import csv
import string

# !*TODO*! Error checking! On the list: 
# - Make sure invalid input messages are helpful and instructions are clear
# - Check that EVERY INPUT is properly safeguarded

# TODO(EXPAND BELOW PROGRAM DESCRIPTION)
#  This program requires the relevant .csv files to be stored in a folder within the main directory entitled "subjects"
    
   
def main():
    # Main() initiates the flashcard session and then acts as a main menu from which the user decides which 
    # of the program's functions they want to undertake. All of the functions return the user to this main 
    # menu once completed so that the user can take perform another function or exit.

    # Initiate the desired subject and save relevant variables to be used by main functions
    print("\nWelcome to flashcards.py! Before we begin, please pick a subject from the list:\n")
    subject = choose_subject()
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
                print("\nWould you like to review cards individually, or print them all at once?\n- Submit 'ONE' to view individual cards\n- Submit 'ALL' to view all cards at once")
                view = choose("Submit: ", 'ONE', 'ALL')
                if view == 'ONE':  
                    # List the card titles with index numbers
#TODO ERROR CHECK for if there are somehow no cards
                    print("\nPlease submit the index number for the desired card from the following list:")
                    counter = 1
#NOTE subject.card_list may be unnecessary
                    for sub_card in subject.card_list:
                        print(f"- {counter} - {string.capwords(sub_card['card_title'])}")
                        counter += 1

                    # Take numeric imput and adjust it to index the list, then print the card
                    pick = val_num_input("Card Number: ", subject.card_list) - 1  
                    rev_card = Card(subject.card_list[pick])
                    print(rev_card)
                
                elif view == 'ALL':
                    # Print every card in the list
                    for card in subject.card_list:
                        rev_card = Card(card)
                        print(rev_card)   

                # Prompt the user to review another card or return to the main menu
                print("What would you like to do next?")
                next = choose("Submit 'AGAIN' to try again or 'RETURN' to go back to the top menu: ", 'AGAIN', 'RETURN')
                if next == 'AGAIN':
                    continue
                elif next == 'RETURN':
                    break
            continued = 1
            continue

        elif task == 'TEST':
            # Give detailed instructions on how to answer, including multiple correct answers
            print("\n- -- Test Instructions -- -\nEach multiple choice question will be randomly generated from one of the fields on each card. Simply input the numeral of the correct answer. For questions with multiple correct answers, input each correct answer one at a time.\n")
            
            # Generate a random question for each card in a random order, tracking correct answers
            test_list = subject.card_list
            random.shuffle(test_list)
            correct = 0
            q_num = 0
            for _ in test_list:
                q_num += 1
                print(f"Question {q_num}\n")
                if random_q(_, subject):
                    correct += 1

            # Print results and return to menu
            print(f"Results: {correct}/{q_num} correct answers\n")  
            continued = 1
            continue

#TODO ADD doesn't update the subject object used by the program at large! It only updates the csv. I'll have to add functionality
# to the ADD section to update it!
        elif task == 'ADD':
            while True:
                # Generate input prompts based on the current subject for the user to write a new card
                print("\nComplete the prompts to add your new flashcard!\nFor fields with multiple values, input all values at once in a list separated by commas (Example: blue, green, red, etc...)\n(WARNING: Any input separated by commas will count each side of the comma as separate entries, use commas with caution!)")
                add_card = create_card(subject.fields)

                # Allow user to review card before submitting
                print("Would you like to submit the following flashcard?\n")
                print(add_card)
                add = choose("Sumbit? (Y/N): ", 'Y', 'N')
                if add == "Y":
                    try:
                        with open(subject.path, 'a') as csv_file:
#NOTE subject.keys may be unnecessary
                            writer = csv.DictWriter(csv_file, fieldnames=subject.keys)
                            writer.writerow(add_card.card)
                    except FileNotFoundError:
                        raise FileNotFoundError("Somehow you selected a file that doesn't exist. That shouldn't be possible but you did it. Impressive!")
                    subject.card_list.append(add_card.card)
                    print("\nCard officially laminated and added to the folder. What would you like to do now?")
                elif add == "N":
                    print("\nCard officially crumpled up and thrown in the bin. What would you like to do now?")
                
                # Prompt the user to make another card or return to the main menu
                what_now = choose("Submit 'AGAIN' to try again or 'RETURN' to go back to the top menu: ", 'AGAIN', 'RETURN')
                if what_now == 'AGAIN':
                    continue
                elif what_now == 'RETURN':
                    break
            continued = 1
            continue

        elif task == 'CHANGE':
            # Choose new subject and redeclare all relevant variables
            subject = choose_subject()
            continued = 1
            continue

        elif task == 'CREATE':
            print("\nIn order to create a subject, you'll need a subject name, the information fields you want to be tested on, and one full flashcard to start it off. Follow these step by step instructions, and don't worry, you'll get a chance to review everything at the end!")
            while True:
                # Prompt user for subject name, since it will be used as a file name it is first cleaned and validated
                new_subject = input("\nFirst, enter the name of the new subject you wish to add\nSubject: ")
                sani_subject = sanitize_filename(new_subject)
                if new_subject != sani_subject:
                    print(f"Your subject name contained some invalid characters that had to be removed. Is this subject name ok?\nNew name: {string.capwords(sani_subject)}")
                    val_sub = choose("Sumbit? (Y/N): ", 'Y', 'N')
                    if val_sub == 'Y':
                        new_subject = sani_subject
                    elif val_sub == 'N':
                        print("Do you want to retry your subject submission?")
                        retry = choose("Submit 'AGAIN' to try again or 'RETURN' to go back to the top menu: ", 'AGAIN', 'RETURN')
                        if retry == 'AGAIN':
                            continue
                        elif retry == 'RETURN':
                            break

                # Prompt user for the new subject's fields and clean them
                new_fields = input("\nNext, input the names of each field you wish the subject to contain in a single list separated by commas (Ex. color, shape, size)\nFields: ").split(",")
                for _ in range(len(new_fields)):
                    if new_fields[_] == "":
                        new_fields.remove(new_fields[_])
                    else:
                        new_fields[_] = new_fields[_].strip()

                # Prompt user to generate a card with the new fields then check with user that all entered data is valid
                print("\nFinally, fill out your new subject's first flashcard")
                new_card = create_card(new_fields)
                print("Would you like to initiate your new subject using the following flashcard? Once you have it will be availble to select from the list of subjects by typing 'CHANGE' into the main menu.\n")
                print(f"- -- {string.capwords(new_subject)} -- -\n")
                print(new_card)
                okay = choose("Create Subject? (Y/N): ", 'Y', 'N').strip()

                # After reviewing data, allow user to submit the new subject, retry, or exit
                if okay == "Y":
                    fieldnames = ["card_title"]
                    fieldnames.extend(new_fields)
                    with open(f"subjects/{new_subject.replace(' ', '_').lower()}.csv", 'w') as csv_file:
                        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerow(new_card.card)
                    break
                elif okay == "N":
                    try_again = choose("Submit 'AGAIN' to try again or 'RETURN' to go back to the top menu: ", 'AGAIN', 'RETURN')
                    if try_again == "AGAIN":
                        continue
                    elif try_again == "RETURN":
                        break
            continued = 1
            continue

        elif task == 'EXIT':
            sys.exit("\nThat was gorgeous, you're gorgeous, stay gorgeous.\n")
        else:
            print("Invalid input, let's try that again shall we?")
            continued = 0
            continue

#NOTE This cardlist is NOT THE TEST CARDLIST, so this should be changed to take the Subject object as an argument
#def random_q(card, subject):
def random_q(card, subject):
    # Random_q creates a randomly generated question for a given card, returning True for a correct answer and False 
    # for and incorrect answer

    # Set the title and fields as variables and pick a random field to generate a question from
    q_card = Card(card)
    q = random.randint(0, len(subject.fields)-1)
    field = subject.fields[q]

    # Obtain the multiple choice options and generate the question, adjusting for single or multiple correct options
#NOTE GET_LIST IS something I can put in the Subject class
    options, correct = get_list(q_card, subject, field)
    print(f"- -- Card: {string.capwords(q_card.title)} -- -")
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
                print(q_card)
        else:
            print("\nIncorrect! Here's the real info:")
            print(q_card)
            return False
    return True


def choose_subject():
    # Choose_subject presents a list of all .csv files located in the subjects folder and allows the user to 
    # select one, returning the path to said file as well as the list of dictionaries and the column names which 
    # are then fed into main's other functions 
    
    # Retrieve path to the folder by adding the folder name to the main directory path
    script_dir = os.path.dirname(__file__)
    s = "subjects"
    path = os.path.join(script_dir, s)

    # Get file names from folder and print them one by one, properly formatted, with index numbers
    file_names = os.listdir(path)
    counter = 1
    print("Subjects:\n")
    for file in file_names:
        if file.endswith(".csv"):
            print(f"- {counter} - {string.capwords(file.removesuffix('.csv').replace('_', ' '))}")
            counter += 1

    # Take the numeric input to index the list and generate the file path as a string, then return that string, the 
    # list of cards, and the keys
    choice = val_num_input("\nEnter the corresponding number for your desired subject: ", file_names) - 1
    subject = "/".join([s, file_names[choice]])
    try:
        with open(subject, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            card_list = list(csv_reader)
            keys = csv_reader.fieldnames
    except FileNotFoundError:
        raise FileNotFoundError("Somehow you selected a file that doesn't exist. That shouldn't be possible but you did it. Impressive!")
    if 'card_title' not in keys:
        raise Exception("CSV File not properly formatted - Missing 'card_title'")

    return Subject(subject, card_list, keys)


def create_card(fields):
    # Create_card takes a subject's fields and generated an input prompt for each one, checking for valid formating 
    # and returning a properly structured dictionary
    
# NOTE include warning about not using the @ symbol, maybe pick a better symbol?
    while True:
        # Create and empty dict and begin setting variables
        card = {}
        card["card_title"] = input("Card Title: ").strip().lower()
        retry = False
        for field in fields:
            # Fields are invalid if the are empty or contain an @ symbol
            if field != "":
                value = input(f"{string.capwords(field)}: ")
            if "@" in value:
                print("Please don't include '@' character in your entry, it jams me up good")
                retry = True
                break
            elif value == "":
                print("Please don't leave any selection blank, input 'none' instead")
                retry = True
                break

            # Handle multiple values by converting to my formatting
            entry = convert_split(value)
            card[field] = entry
        
        # If field input is invalid, automatically reprompts
        if retry == True:
            print("Let's try that again....\n")
            continue
        return Card(card)


def choose(prompt, arg1, arg2):
    # Choose automates asking a prompt in a while loop to allow reprompting, returning only one of the correct options
    while True:
        choice = input(prompt).strip()
        if choice not in [arg1, arg2]:
            print("Invalid input. Please only input one of the stated options\n")
            continue
        else:
            break
    if choice == arg1:
        return arg1
    else:
        return arg2


if __name__ == "__main__":
    main()