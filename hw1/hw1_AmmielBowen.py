"""
CIS-4930 Introduction to Python, Spring 2026
Homework : 1
Student Name: Ammiel Bowen
Student ID: ab22dv
Section: 0003
Submission Date: 02-02-2026
"""

# --------------------------------------------------
# Problem 1: Campus WiFi Access Log Analyzer
# --------------------------------------------------

wifi_logs = [
    ("LIB", 45, 9),
    ("LIB", 92, 11),
    ("CSC", 67, 14),
    ("LIB", 78, 13),
    ("ENG", 120, 10),
    ("CSC", 55, 15),
    ("ENG", 89, 16)
]

# Unique buildings with >50 devices
busy_buildings = {b for b, d, h in wifi_logs if d > 50}
print("Busy buildings (>50):", busy_buildings)

# Peak hours ≥80 devices
peak_hours = [(b, d, h) for b, d, h in wifi_logs if d >= 80]
print("Peak hours (≥80):", peak_hours)

# Library device slices
library_devices = [d for b, d, h in wifi_logs if b == "LIB"]
print("Library slices:", library_devices)

# Busiest building by average
totals = {}
counts = {}

for b, d, h in wifi_logs:
    totals[b] = totals.get(b, 0) + d
    counts[b] = counts.get(b, 0) + 1

busiest = ""
highest_avg = 0

for b in totals:
    avg = totals[b] / counts[b]
    if avg > highest_avg:
        highest_avg = avg
        busiest = b

print(f"Busiest: {busiest} (avg {highest_avg:.1f} devices)")


# --------------------------------------------------
# Problem 2: University Course Planner
# --------------------------------------------------

catalog = {
    "CIS-4930": {"title": "Introduction to Python", "credits": 3, "prereqs": ["COP-3014", "COP-3330"]},
    "COP-3014": {"title": "Programming I in C++", "credits": 3, "prereqs": []},
    "COP-3330": {"title": "Object Oriented Programming", "credits": 3, "prereqs": []},
    "CIS-3014": {"title": "Intro to Computing", "credits": 3, "prereqs": []},
    "CIS-3250": {"title": "Web Development", "credits": 3, "prereqs": ["CIS-3014"]}
}

code = input("Enter course code: ")

if code in catalog:
    course = catalog[code]
    print(f"{code}: {course['title']} ({course['credits']} credits)")

    if course["prereqs"]:
        print("Prerequisites:", ", ".join(course["prereqs"]))
    else:
        print("Prerequisites: None")

    total_credits = course["credits"]
    for p in course["prereqs"]:
        if p in catalog:
            total_credits += catalog[p]["credits"]

    print("Total credits with prereqs:", total_credits)
else:
    print("Course not found.")


# --------------------------------------------------
# Problem 3: Cafeteria Menu & Order Validator
# --------------------------------------------------

menu = {
    "burger": {"price": 5.50, "category": "main"},
    "fries": {"price": 2.00, "category": "side"},
    "soda": {"price": 1.50, "category": "drink"},
    "salad": {"price": 4.00, "category": "side"}
}

print("Menu:")
for item in menu:
    print(f"{item} (${menu[item]['price']:.2f})")

order = []
n = int(input("How many different items? "))

for i in range(n):
    name = input("Item name: ")
    qty = int(input("Quantity: "))
    order.append({"item": name, "qty": qty})

total = 0.0

print("\nOrder:")
for o in order:
    item = o["item"]
    qty = o["qty"]

    if item in menu:
        price = menu[item]["price"]
        line = price * qty
        total += line
        print(f"{item} x{qty} @ ${price:.2f} = ${line:.2f}")
    else:
        print(f"Item '{item}' not on menu, skipping.")

print("--------------")
print(f"Total: ${total:.2f}")
