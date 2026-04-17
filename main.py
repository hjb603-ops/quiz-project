import csv
import os

# quiz system project - adaptive difficulty based on user performance
# simple quiz system with adaptive difficulty
def load_questions(file_name):
    # load questions from csv file
    question_list = []

    try:
        with open(file_name, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                q = {
                    "difficulty": row["difficulty"],
                    "question": row["question"],
                    "options": [
                        row["option1"],
                        row["option2"],
                        row["option3"],
                        row["option4"]
                    ],
                    "answer": row["answer"]
                }
                question_list.append(q)

    except:
        print("error loading questions file")

    return question_list


def filter_by_difficulty(question_list, level):
    # get questions based on difficulty
    filtered_list = []

    for q in question_list:
        if q["difficulty"] == level:
            filtered_list.append(q)

    return filtered_list


def ask_question(q):
    print("\nDifficulty:", q["difficulty"])
    print(q["question"])

    for i in range(len(q["options"])):
        print(str(i + 1) + ".", q["options"][i])

    # input validation
    while True:
        answer_input = input("Enter answer (1-4): ")

        if answer_input >= "1" and answer_input <= "4":
            break
        else:
            print("invalid input, try again")

    if answer_input == q["answer"]:
        print("correct")
        return True
    else:
        correct_index = int(q["answer"]) - 1
        print("wrong, correct answer:", q["options"][correct_index])
        return False


def update_difficulty(level, correct):
    # change difficulty based on answer
    if correct:
        if level == "easy":
            return "medium"
        elif level == "medium":
            return "hard"
        else:
            return "hard"
    else:
        if level == "hard":
            return "medium"
        elif level == "medium":
            return "easy"
        else:
            return "easy"


def save_result(file_name, user_name, user_score, total):
    file_exists = os.path.exists(file_name)

    try:
        with open(file_name, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            if not file_exists or os.path.getsize(file_name) == 0:
                writer.writerow(["name", "score", "total"])

            writer.writerow([user_name, user_score, total])

    except:
        print("error saving score")


def view_scores(file_name):
    try:
        with open(file_name, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            print("\nall scores")
            print("----------------")

            empty = True

            for row in reader:
                print(row["name"], "-", row["score"] + "/" + row["total"])
                empty = False

            if empty:
                print("no scores yet")

    except:
        print("file not found")


def search_scores(file_name, name_to_find):
    try:
        with open(file_name, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            print("\nsearch results")
            print("----------------")

            found = False

            for row in reader:
                if row["name"].lower() == name_to_find.lower():
                    print(row["name"], "-", row["score"] + "/" + row["total"])
                    found = True

            if not found:
                print("no match found")

    except:
        print("file not found")


def top_scores(file_name):
    results = []

    try:
        with open(file_name, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                results.append(row)

        results.sort(key=lambda x: int(x["score"]), reverse=True)

        print("\ntop scores")
        print("----------------")

        for row in results:
            print(row["name"], "-", row["score"] + "/" + row["total"])

    except:
        print("error reading scores")


def score_chart(file_name):
    # simple text chart
    try:
        with open(file_name, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            print("\nscore chart")
            print("----------------")

            for row in reader:
                name = row["name"]
                score = int(row["score"])
                print(name + ":", "*" * score)

    except:
        print("no data for chart")


def run_quiz():
    questions = load_questions("questions.csv")

    if len(questions) == 0:
        print("no questions found")
        return

    user_name = input("Enter your name: ")

    while user_name.strip() == "":
        print("name cannot be empty")
        user_name = input("Enter your name: ")

    user_score = 0
    num_questions = 5
    difficulty = "easy"

    used_questions = []

    for i in range(num_questions):
        available = filter_by_difficulty(questions, difficulty)

        chosen = None

        for q in available:
            if q not in used_questions:
                chosen = q
                break

        if chosen is None:
            for q in questions:
                if q not in used_questions:
                    chosen = q
                    break

        if chosen is None:
            break

        used_questions.append(chosen)

        correct = ask_question(chosen)

        if correct:
            user_score += 1

        difficulty = update_difficulty(difficulty, correct)

    print("")
    print("quiz finished")
    print("score:", user_score, "/", num_questions)

    save_result("scores.csv", user_name, user_score, num_questions)


def menu():
    while True:
        print("\nWelcome to the Quiz System")
        print("1. start quiz")
        print("2. view scores")
        print("3. search scores")
        print("4. top scores")
        print("5. score chart")
        print("6. exit")

        choice = input("choose option: ")

        if choice == "1":
            run_quiz()
        elif choice == "2":
            view_scores("scores.csv")
        elif choice == "3":
            name = input("enter name: ")
            search_scores("scores.csv", name)
        elif choice == "4":
            top_scores("scores.csv")
        elif choice == "5":
            score_chart("scores.csv")
        elif choice == "6":
            print("exiting...")
            break
        else:
            print("invalid option")


menu()