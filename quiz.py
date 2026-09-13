import json
import os
import random


#Question
def addquestion(question, answer):
    "Adding question to the database"
    try:
        with open('questions.txt', 'w') as f:
            if os.path.getsize('questions.txt') == 0:
                row = f"1. {question}; {answer}\n"
                f.write(row)
            else:
                rows = f.readlines()
                first_symbol = rows[-1][0]
                row = f"{int(first_symbol)+1}. {question}; {answer}\n"
                f.write(row)
    except:
        print("Error with opening file")

    f.close()


def removequestion(index):
    "Removing question from the database"
    try:
        with open('questions.txt', 'r') as f:
            rows = f.readlines()

            if 0 <= index < len(rows):
                del rows[index]
                f.writelines(rows)
            else:
                print("index out of range")
    except:
        print("Error with opening file")


# Player
def register(username, password, pass_again):
    "Functional side of user registration"
    if password == pass_again:
        user = {"username": username, "password": password}
        try:
            with open('users.json', 'r') as f:
                users = json.load(f)
                for existing_user in users:
                    if existing_user["username"] == username:
                        print("Uživatelské jméno je již obsazené.")
                        return None

        except (FileNotFoundError, json.JSONDecodeError):
            users = []

        users.append(user)

        with open('users.json', 'w') as f:
            json.dump(users, f, indent=2)

        return username

    else:
        print("Password mismatch")


def login(username, password):
    "Functional side of user login"
    try:
        with open('users.json', 'r') as f:
            users = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("File not found.")
        return None

    for user in users:
        if user["username"] == username and user["password"] == password:
            print("Login successful.")
            return user

    print("Invalid username or password.")
    return None


def registrationui():
    "Interactive side of user registration"
    print("Registration")
    username = input("Username: ")
    password = input("Password: ")
    pass_again = input("Password again: ")
    return register(username, password, pass_again)


def loginui():
    "Interactive side of user login"
    print("Login")
    username = input("Username: ")
    password = input("Password: ")
    return login(username, password)
# Quiz

# MainUI
# GenerateQuestions
# PlayerScores
# startquiz