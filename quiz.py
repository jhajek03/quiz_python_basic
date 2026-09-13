import json
import os
import random


#Question
def addquestion(question, answer):
    """Adding question to the database"""
    try:
        with open("questions.txt", "r", encoding="utf-8") as f:
            rows = f.readlines()

        if not rows:
            number = 1
        else:
            number = int(rows[-1].split(".")[0]) + 1

        with open("questions.txt", "a", encoding="utf-8") as f:
            f.write(f"{number}. {question}; {answer}\n")

    except Exception as e:
        print("Error with opening file:", e)


def removequestion(index):
    """Removing question from the database"""
    try:
        with open("questions.txt", "r", encoding="utf-8") as f:
            rows = f.readlines()

        if 0 <= index < len(rows):
            del rows[index]

            with open("questions.txt", "w", encoding="utf-8") as f:
                f.writelines(rows)
        else:
            print("index out of range")

    except Exception as e:
        print("Error with opening file:", e)

# Player
def register(username, password, pass_again):
    "Functional side of user registration"
    if password == pass_again:
        user = {"username": username, "password": password, "best-score": 0}
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
            json.dump(users, f, indent=3)

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
            return user["username"]

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
def setscore(username, score):
    try:
        with open("users.json", "r", encoding="utf-8") as f:
            users = json.load(f)

        for user in users:
            if user["username"] == username:

                if user["best-score"] < score:
                    user["best-score"] = score
                    print(f"New best score! {score} points!")

                    with open("users.json", "w", encoding="utf-8") as f:
                        json.dump(users, f, indent=4)

                return user["best-score"]

        print("User not found")

    except Exception as e:
        print("Error:", e)


def quizui(username):
    try:
        with open('questions.txt', 'r',encoding="utf-8") as f:
            questions = f.readlines()
            draw = random.sample(range(1, len(questions)), 5)
            score = 0

            for question in draw:
                drawn_question, correct_answer = questions[question].strip().split(";")

                print(drawn_question)
                answer = input("your answer: ")

                if answer == correct_answer:
                    print("Correct!")
                    score += 1
                else:
                    print("Wrong!")
                    print("Correct Answer:", correct_answer)

            setscore(username, score)
            print(f"Your score is {score}")
            return score

    except FileNotFoundError:
        print("File not found.")


def questionui():
    ui = input("1 ... Add\n2 ... Remove\n3 ... Exit\nChoose a number: ")

    if ui == "1":
        question = input("Question: ")
        answer = input("Answer: ")
        addquestion(question, answer)

    elif ui == "2":
        removequestion(int(input("Choose index: ")))


def print_leaderboard():
    with open("users.json", "r", encoding="utf-8") as f:
        users = json.load(f)

    sorted_users = sorted(users, key=lambda x: x["best-score"], reverse=True)

    for i, user in enumerate(sorted_users, start=1):
        print(f"{i}. {user['username']}: {user['best-score']} points")



# MainUI
def mainui(username="guest"):
    while True:
        print(f"Welcome {username}")

        if username == "guest":
            ui = input("1 ... Register\n2 ... Login\n5 ... Leaderboard\n 6 ... Exit\nChoose a number: ")
        else:
            ui = input("1 ... Register\n2 ... Login\n3 ... Edit Questions\n4 ... Start Quiz\n5 ... Leaderboard\n 6 ... Exit\nChoose a number: ")

        if ui == "1":
            registrationui()

        elif ui == "2":
            mainui(loginui())

        elif ui == "3" and not username == "guest":
            questionui()

        elif ui == "4" and not username == "guest":
            quizui(username)

        elif ui == "5":
            print_leaderboard()

        elif ui == "6":
            break

        else:
            print("Invalid input")


if __name__ == "__main__":
    mainui()