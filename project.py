import os
import sys
import random
import csv
import string
from extras import create_card, random_q, the, val_num_input


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
        print("\n  - -- Menu -- -\n- Submit 'REVIEW' to review flashcards\n- Submit 'TEST' to take the test\n- Submit 'ADD' to add a flashcard\n- Submit 'CHANGE' to change subjects\n- Submit 'CREATE' to create a new subject\n- Submit 'EXIT' to exit the program")
        task = input("\nSubmit: ").strip()
        if task == 'REVIEW':
            review_cards(subject)
            continued = 1
            continue
        elif task == 'TEST':
            run_test(subject)
            continued = 1
            continue
        elif task == 'ADD':
            add_card(subject)
            continued = 1
            continue
        elif task == 'CHANGE':
            subject = choose_subject()
            continue
        elif task == 'CREATE':
            create_subject()
            continue
        elif task == 'EXIT':
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
        try:
            with open(subject, mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                keys = csv_reader.fieldnames
        except FileNotFoundError:
            raise FileNotFoundError("Somehow you selected a file that doesn't exist. That shouldn't be possible but you did it. Impressive!")

        # Gather fields directly from the keys list to preserve the correct order
        fields = list(keys)
        fields.remove('card_title')

        # Run create_card to collect inputs for each field
        print("\nComplete the prompts to add your new flashcard!\nFor fields with multiple values, input all values at once in a list separated by commas (Example: blue, green, red, etc...)\n(WARNING: Any input separated by commas will count each side of the comma as separate entries, use commas with caution!)")
        card = create_card(fields)

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


def create_subject():
    # This function will act similarly to the add card but will write a whole new csv to the subjects folder.
    #TODO ERROR CHECK AND TEST, THEN ADD MORE DESCRIPTIONS 
    print("INSERT FUNCTION DESCRIPTION HERE")#TODO
    while True:
        subject = input("\nFirst, enter the name of the new subject you wish to add\nSubject: ")
        fields = input("\nNext, input the names of each field you wish the subject to contain in a single list separated by commas (Ex. color, shape, size)\nFields: ").split(",")
        #NOTE unsure about the folowing syntax
        for field in fields:
            field = field.strip()
        card = create_card(fields)

         # Check with user that all entered data is valid
        print("Would you like to initiate your new subject using the following flashcard?\n")
        print(f"- -- {string.capwords(subject)} -- -\n")
        print(the(card))
        while True:
            okay = input("Create Subject? (Y/N): ").strip()

            # Allow user to submit, retry, or exit after reviewing data
            if okay == "Y":
                fields.append("card_title")
                with open(f"subjects/{subject.replace(' ', '_').lower()}.csv", 'w') as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=fields)
                    writer.writeheader()
                    writer.writerow(card)
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


if __name__ == "__main__":
    main()