from extras import create_card, random_q, the, val_num_input
import os
import sys
import random
import csv
import string

#TODO CHECK GIVEN INSTRUCTIONS ARE THOROUGH, ADD ERROR CHECKING, FIGURE OUT HOW TO IMPLEMENT TEST_PROJECT.PY(FIGURE OUT EXACTLY HOW TO ASK FOR ADVICE ON THIS FROM R/CS50)
# TODO(EXPAND BELOW PROGRAM DESCRIPTION)
#  This program requires the relevant .csv files to be stored in a folder within the main directory entitled "subjects"
    
   
def main():
    # Main() initiates the flashcard session and then acts as a main menu from which the user decides which 
    # of the program's functions they want to undertake. All of the functions return the user to this main 
    # menu once completed so that the user can take perform another function or exit.

    # Begin by initiating the desired subject
    print("\nWelcome to flashcards.py! Before we begin, please pick a subject from the list:\n")
    subject = choose_subject()

    # Upon opening the program, ask if the user wants to take a test or add a new flashcard
    print("\nWhat a delightful choice! What would you like to do now?")
    
    # Set variable to track if any tasks have been completed
    continued = 0
    while True:

        # Only includes this prompt if any task has already been completed
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
            continued = 1
            continue
        elif task == 'CREATE':
            create_subject()
            continued = 1
            continue
        elif task == 'EXIT':
            sys.exit("\nThat was gorgeous, you're gorgeous, stay gorgeous.\n")
        else:
            print("Invalid input, let's try that again shall we?")
            continued = 0
            continue


def review_cards(subject):
    # Review_cards() allows users to view the cards for the selected subject directly, either one at a time or 
    # all at once. After viewing the selection the user is prompted to either review another selection or return 
    # to the main menu.

    # Read csv file with flashcard data into a list
    try:
        with open(subject, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            card_list = list(csv_reader)
    except FileNotFoundError:
        raise FileNotFoundError("Somehow you selected a file that doesn't exist. That shouldn't be possible but you did it. Impressive!")

    # Prompt user to review either an individual card or all cards simultaneously
    while True:
        print("\nWould you like to review cards individually, or print them all at once?\n- Submit 'ONE' to view individual cards\n- Submit 'ALL' to view all cards at once")
        view = input("Submit: ")

        # List the card titles with index numbers
        if view == "ONE":    
            print("\nPlease submit the index number for the desired card from the following list:")
            counter = 1
            for card in card_list:
                print(f"- {counter} - {string.capwords(card['card_title'])}")
                counter += 1

            # Take numeric imput and adjust it to index the list, then print the card
            pick = val_num_input("Card Number: ", card_list) - 1
            print(the(card_list[pick]))

        # Iterate over the whole list to print every card
        elif view == "ALL":
            for card in card_list:
                print(f"\n{the(card)}")

        # Basic error catching
        else:
            print("Invalid input, let's try that again shall we?")
            continue

        # After reviewing desired cards, either continue reviewing or return to main function
        next = input("Submit 'AGAIN' to continue reviewing, or submit 'RETURN' to return to the top menu: ")
        if next == 'AGAIN':
            continue
        elif next == 'RETURN':
            return


# TODO Error checking
def run_test(subject):
    # Run_test() creates a fully randomized test of the flashcards for the user. The order of the cards is 
    # randomized, as well as the specific field the user will be tested on for each flashcard. Multiple-
    # -choice questions are generated using random_q by taking the correct answer(s) and shuffling it(them) 
    # into a list of wrong answers, generated from the entries for that field on other flashcards. One question
    # is asked per card and the full card is displayed for review after each question regardless of the answer.
    # After the test the results are given and the user is returned to the main menu.

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
    # Add_card() allows the user to update a subject with a new flashcard. It retrieves the fieldnames from the
    # current subject and feeds them to the create_card function which handles collecting the user input into a 
    # dictionary which can be written into the .csv file. The card input into the() and printed for the user's 
    # review to submit or not. Regardless, the user is prompted to either make another new card or return to menu

    while True:
        # Get to iterate over and use as fieldnames argument when writing csv 
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

            # Allow user to choose to submit the card or not after reviewing data
            if okay == "Y":
                try:
                    with open(subject, 'a') as csv_file:
                        writer = csv.DictWriter(csv_file, fieldnames=keys)
                        writer.writerow(card)
                except FileNotFoundError:
                    raise FileNotFoundError("Somehow you selected a file that doesn't exist. That shouldn't be possible but you did it. Impressive!")
                print("\nCard officially laminated and added to the folder. What would you like to do now?")
            elif okay == "N":
                print("\nCard officially crumpled up and thrown in the bin. What would you like to do now?")
            else:
                print("Invalid input. C'mon now it's just one letter, you can do it!\n")
                continue

            # Prompt the user to make another card or return to the main menu
            what_now = input("Submit 'AGAIN' to add a new card or 'RETURN' to go back to the top menu: ")
            if what_now == "AGAIN":
                break
            elif what_now == "RETURN":
                return
            else:
                print("Invalid input. Let's try that one again, shall we?\n")
                continue
        continue


def choose_subject():
    # Choose_subject() presents a list of all .csv files located in the subjects folder and allows the user to 
    # select one, returning the path to said file which is then fed into main's other functions. 
    
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

    # Take the numeric input to index the list and generate the file path as a string, then return that string
    choice = val_num_input("\nEnter the corresponding number for your desired subject: ", file_names) - 1
    subject = "/".join([s, file_names[choice]])
    return subject


def create_subject():
    # Create_subject() allows users to add a new .csv file to the subjects folder by defining the subject, it's 
    # fields, and defining single flashcard as reference so that a subject always has at least one card in it.
    # As in the add_card function, the full card and subject are displayed for review and if unsatisfactory, the
    # user is prompted to retry or return to the main menu. Unlike add_card, if the subject is submitted the 
    # user is returned straight to the main menu, as it's less likely they'll want to add mulitple new subjects
    # to the folder than multiple new cards to a subject.

    # Print instructions and take input for the new subject and fields
    print("\nIn order to create a subject, you'll need a subject name, the information fields you want to be tested on, and one full flashcard to start it off. Follow these step by step instructions, and don't worry, you'll get a chance to review everything at the end!")
    while True:
        subject = input("\nFirst, enter the name of the new subject you wish to add\nSubject: ")
        fields = input("\nNext, input the names of each field you wish the subject to contain in a single list separated by commas (Ex. color, shape, size)\nFields: ").split(",")

        # Clean data and create new flashcard
        for field in fields:
            field = field.strip()
        print("\nFinally, fill out your new subject's first flashcard")
        card = create_card(fields)

         # Check with user that all entered data is valid
        print("Would you like to initiate your new subject using the following flashcard?\n")
        print(f"- -- {string.capwords(subject)} -- -\n")
        print(the(card))
        while True:
            okay = input("Create Subject? (Y/N): ").strip()

            # After reviewing data, allow user to submit the new subject, retry, or exit
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