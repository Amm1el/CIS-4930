"""
CIS-4930 Introduction to Python, Spring 2026
Homework : 0
Student Name: Ammiel Bowen
Student ID: ab22dv
Section: 0003
Submission Date: 01-22-2026
"""

# --------------------------------------------------
# Problem 1: Planetary Cargo Weight Checker
# --------------------------------------------------

planet = input("Enter destination planet (Earth, Moon, Mars): ").lower()
num_items = int(input("Enter number of items: "))

total_weight = 0.0

for i in range(num_items):
    weight = float(input(f"Enter weight of item {i + 1} (kg): "))
    total_weight += weight

if planet == "earth":
    maximum = 500
elif planet == "moon":
    maximum = 300
elif planet == "mars":
    maximum = 250
else:
    maximum = 0  # invalid planet safety

print(f"Total weight: {total_weight:.2f} kg")

if total_weight <= maximum:
    print("Status: OK")
else:
    print("Status: OVER LIMIT")


# --------------------------------------------------
# Problem 2: Astronaut Training Fatigue Tracker
# --------------------------------------------------

hours = int(input("Enter number of hours tracked: "))

max_fatigue = 0
dangerous = 0
increases = 0

previous = None

for i in range(hours):
    fatigue = int(input(f"Enter fatigue level for hour {i + 1}: "))

    if fatigue > max_fatigue:
        max_fatigue = fatigue

    if fatigue > 8:
        dangerous = 1

    if previous is not None and fatigue > previous:
        increases += 1

    previous = fatigue

if dangerous == 1:
    classification = "HIGH RISK - Medical review required"
elif increases > 3:
    classification = "MODERATE RISK - Extra rest recommended"
else:
    classification = "NORMAL - Proceed"

print(f"Hours tracked: {hours}, Max fatigue: {max_fatigue}, Dangerous hours: {dangerous}, Increases: {increases}")
print(f"Training day classification: {classification}")


# --------------------------------------------------
# Problem 3: Interactive Dungeon Door Code Puzzle
# --------------------------------------------------

energy = 0

while energy < 50:
    entry = input("Enter an integer (or 'quit' to give up): ")

    if entry == "quit":
        break

    value = int(entry)
    energy += value

    if energy < 0:
        print("Door resets!")
        energy = 0

if energy >= 50:
    print(f"Door opens with energy {energy}")
else:
    print(f"You gave up with energy {energy}")


# --------------------------------------------------
# Problem 4: Librarian's Overdue Book Fine Calculator
# --------------------------------------------------

book_type = input("Enter book type (novel, textbook, childrens): ").lower()
days = int(input("Enter days overdue: "))
age = int(input("Enter borrower age: "))

if book_type == "novel":
    rate = 0.25
elif book_type == "textbook":
    rate = 0.50
elif book_type == "childrens":
    rate = 0.125
else:
    print("Unknown type; using novel rate")
    rate = 0.25
    book_type = "novel"

base_fine = rate * days
discount = 0.0
long_fee = 0.0

if age < 12:
    discount = base_fine * 0.5

if days > 30:
    long_fee = 5.0

total = base_fine - discount + long_fee
if total < 0:
    total = 0.0

print(f"Book: {book_type.capitalize()}, Days overdue: {days}, Borrower age: {age}")
print(f"Base fine: ${base_fine:.2f}")
print(f"Youth discount applied: -${discount:.2f}")
print(f"Long overdue fee: ${long_fee:.2f}")
print(f"Total due: ${total:.2f}")


# --------------------------------------------------
# Problem 5: Guess the Number with Adaptive Hints
# --------------------------------------------------

secret = 73
guesses = 0

while True:
    guess = int(input("Enter your guess: "))
    guesses += 1

    diff = abs(guess - secret)

    if guess == secret:
        print(f"Correct! You found it in {guesses} guesses.")
        break
    elif diff <= 5:
        hint = "Very close!"
    elif diff <= 15:
        hint = "Warm."
    else:
        hint = "Cold."

    if guess > secret:
        direction = "Too high"
    else:
        direction = "Too low"

    print(f"{hint} {direction}.")

print(f"Secret number: {secret}, your final guess: {guess}, total guesses: {guesses}.")