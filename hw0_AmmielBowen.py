"""
CIS-4930 Introduction to Python, Spring 2026
Homework : 0
Student Name: Ammiel Bowen
Student ID: ab22dv
Section: 0003
Submission Date: 01-23-2026
"""

# ------------------------------------------
# Problem 1: Planetary Cargo Weight Checker

planet = input("Enter destination (Earth, Moon, Mars): ").lower() # Additional Twist .lower() and prints text / asks for starting input
num_items = int(input("Enter number of items: ")) # Prints text / asks input for number of items

total_weight = 0.0 # initializes total weight at 0 before for loop

for i in range(num_items): # for loop based off number of items
    weight = float(input(f"Enter weight of item {i + 1} in kg: ")) # Allows us to continuously add 
    total_weight += weight # continuously adds weight to total_weight

if planet == "earth": # if, elif, else statements for what the maximum weight should be
    maximum = 500
elif planet == "moon":
    maximum = 300
elif planet == "mars":
    maximum = 250
else:
    maximum = 0  # invalid

print(f"Total weight: {total_weight:.2f} kg") #prints total weight in kg rounded to 2 decimal points

if total_weight <= maximum: # if weight less than max OK, else OVER LIMIT
    print("Status: OK")
else:
    print("Status: OVER LIMIT")


# ----------------------------------------------
# Problem 2: Astronaut Training Fatigue Tracker

hours = int(input("Enter number of hours tracked: ")) #input for number of hours tracked

max_fatigue = 0 #initializing variables
dangerous = 0
increases = 0

previous = None #initializes a variable that does not have a value yet and will be used with fatigue

for i in range(hours): # for loop over amount of hours that will be tracked
    fatigue = int(input(f"Enter fatigue level for hour {i + 1}: ")) #assigns number to fatigue

    if fatigue > max_fatigue: # constantly replaces max_fatigue with highest amount of fatigue
        max_fatigue = fatigue

    if fatigue > 8: # any reading above 8 at any time is automatically high risk
        dangerous = 1

    if previous is not None and fatigue > previous:
        increases += 1 #does not include the first run through, and after only increases if current fatigue larger than previous fatigue

    previous = fatigue # replace current fatigue (after first run) with last one

if dangerous == 1:
    classification = "HIGH RISK - Medical review required" # if elif else statements for decreasing risk
elif increases > 3:
    classification = "MODERATE RISK - Extra rest recommended"
else:
    classification = "NORMAL - Proceed"

print(f"Hours tracked: {hours}, Max fatigue: {max_fatigue}, Dangerous hours: {dangerous}, Increases: {increases}") # Prints statistics regarding every aspect of program
print(f"Training day classification: {classification}") #prints classification


# ------------------------------------------------
# Problem 3: Interactive Dungeon Door Code Puzzle

energy = 0 # start with energy at 0

while energy < 50: # while loop for as long as it takes for energy to go above 50
    entry = input("Enter an integer (or 'quit' to give up): ")

    if entry == "quit": # breaks out of while loop if quit is typed
        break

    value = int(entry) # turns entry into an integer
    energy += value # adds value to energy

    if energy < 0: # Automatically resets to 0 if energy ever falls below 0
        print("Door resets!")
        energy = 0

if energy >= 50: # If statement after while loop finishes or is broken out of
    print(f"Door opens with energy {energy}") # print statements concluding end of program
else:
    print(f"You gave up with energy {energy}")


# ----------------------------------------------------
# Problem 4: Librarian's Overdue Book Fine Calculator

book_type = input("Enter book type (novel, textbook, childrens): ").lower() # accepts book type disregarding capitalization
days = int(input("Enter days overdue: ")) # input integer for days a book overdue
age = int(input("Enter borrower age: ")) # age of borrower input

if book_type == "novel": # if elif else statements for type of book and the rate
    rate = 0.25
elif book_type == "textbook":
    rate = 0.50
elif book_type == "childrens":
    rate = 0.125
else:
    print("Unknown type; using novel rate") # if does not fit into any category, 'standardize' to novel (challenge)
    rate = 0.25
    book_type = "novel"

base_fine = rate * days # initialize variables for fine, discount, fee
discount = 0.0
long_fee = 0.0

if age < 12: # Discount based on age
    discount = base_fine * 0.5

if days > 30: # fee based on days
    long_fee = 5.0

total = base_fine - discount + long_fee #calculating total
if total < 0: # make it so it can't be a negative
    total = 0.0

print(f"Book: {book_type.capitalize()}, Days overdue: {days}, Borrower age: {age}") # print everything with proper spacing and correct decimals
print(f"Base fine: ${base_fine:.2f}")
print(f"Youth discount applied: -${discount:.2f}")
print(f"Long overdue fee: ${long_fee:.2f}")
print(f"Total due: ${total:.2f}")


# ------------------------------------------------
# Problem 5: Guess the Number with Adaptive Hints

secret = 73 # 'secret' integer
guesses = 0 #document number of guesses from participant

while True: # keeps in loop with no chance of breaking out if you don't guess right number
    guess = int(input("Enter your guess: "))
    guesses += 1

    diff = abs(guess - secret) # difference between guess and the number

    if guess == secret:
        print(f"Correct! You found it in {guesses} guesses.") # prints if secret found
        break
    elif diff <= 5: # less than 5 away prints very close
        hint = "Very close!"
    elif diff <= 15:
        hint = "Warm." # less than 15 away but more than 5 prints warm
    else:
        hint = "Cold." # more than 15 away prints cold

    if guess > secret: #if guess is too high print too high, else too low
        direction = "Too high"
    else:
        direction = "Too low"

    print(f"{hint} {direction}.") # print hint and direction

print(f"Secret number: {secret}, your final guess: {guess}, total guesses: {guesses}.") # prints number, amount of guesses, and final guess (same as secret number)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
