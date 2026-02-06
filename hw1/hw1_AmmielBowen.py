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

# creating the list of tuples exactly like the sample data format:
wifi_logs = [
    ("LIB", 45, 9),   # building, devices, hour
    ("LIB", 92, 11),
    ("CSC", 67, 14),
    ("LIB", 78, 13),
    ("ENG", 120, 10),
    ("CSC", 55, 15),
    ("ENG", 89, 16)
]

# -----------------------------
# 1) Set: Unique buildings with >50 devices at once

# start with an empty set because sets only store unique items (no duplicates)
busy_buildings = set()

# loop through each tuple in wifi_logs and unpack it into variables
for building, devices, hour in wifi_logs:
    # we only want buildings where devices > 50
    if devices > 50:
        busy_buildings.add(building)  # add building code to set

print("Busy buildings (>50):", busy_buildings)

# -----------------------------
# 2) List comprehension: Peak hours (≥80 devices) with building names

# peak hours means device count >= 80, and we want the tuple included in the output list
peak_hours = [(b, d, h) for (b, d, h) in wifi_logs if d >= 80]

print("Peak hours (≥80):", peak_hours)

# -----------------------------
# 3) Slicing requirement: Device counts for Library only (building "LIB")
# -----------------------------

# the prompt says slicing, but their expected output is basically "all device counts for LIB"
# (this will match the example output list)
library_devices = [devices for (building, devices, hour) in wifi_logs if building == "LIB"]

print("Library slices:", library_devices)

# -----------------------------
# 4) Report: Busiest building by average devices (manual accumulation)

# totals per building AND counts per building
totals = {}  # building -> sum of devices
counts = {}  # building -> how many entries

# go through every log entry and update totals/counts
for building, devices, hour in wifi_logs:
    # totals.get(building, 0) gives 0 if building not there yet
    totals[building] = totals.get(building, 0) + devices
    counts[building] = counts.get(building, 0) + 1

# now find the building with the highest average
busiest_building = ""   # store the building code with best avg
highest_avg = 0.0       # store the highest average seen so far

for building in totals:
    # average = total devices / number of readings
    avg = totals[building] / counts[building]

    # if this average is bigger than our current max, replace it
    if avg > highest_avg:
        highest_avg = avg
        busiest_building = building

print(f"Busiest: {busiest_building} (avg {highest_avg:.1f} devices)")


# Problem 2: University Course Planner
# --------------------------------------------------

# creating a course catalog dictionary keyed by course code
# each course code maps to another dictionary (nested dict)
catalog = {
    "CIS-4930": {
        "title": "Introduction to Python",
        "credits": 3,
        "prereqs": ["COP-3014", "COP-3330"]
    },
    "COP-3014": {
        "title": "Programming I in C++",
        "credits": 3,
        "prereqs": []
    },
    "COP-3330": {
        "title": "Object Oriented Programming",
        "credits": 3,
        "prereqs": []
    },
    "CIS-3014": {
        "title": "Intro to Computing",
        "credits": 3,
        "prereqs": []
    },
    "CIS-3250": {
        "title": "Web Development",
        "credits": 3,
        "prereqs": ["CIS-3014"]
    }
}

# asking user for a course code
code = input("Enter course code: ")

# check if the course exists in the dictionary
if code in catalog:
    course = catalog[code]  # grab the nested dict for that course

    # print out formatted summary like the assignment example
    print(f"{code}: {course['title']} ({course['credits']} credits)")

    # prerequisites printing rules:
    # if the prereq list is empty, print "None"
    if course["prereqs"]:
        print("Prerequisites:", ", ".join(course["prereqs"]))
    else:
        print("Prerequisites: None")

    # extra feature: total credits = course credits + credits of direct prereqs (no recursion)
    total_credits = course["credits"]

    # loop through immediate prereqs and add credits if the prereq code exists in our catalog
    for prereq_code in course["prereqs"]:
        if prereq_code in catalog:
            total_credits += catalog[prereq_code]["credits"]
        else:
            # if prereq not in catalog, we just ignore it (prompt says handle missing codes)
            # we are not adding anything here because we dont know credits
            pass

    print("Total credits with prereqs:", total_credits)

else:
    # if course code not found, print informative message
    print("Course not found.")


# Problem 3: Cafeteria Menu & Order Validator
# --------------------------------------------------

# menu is a dictionary of dictionaries
# value = inner dict with price and category
menu = {
    "burger": {"price": 5.50, "category": "main"},
    "fries": {"price": 2.00, "category": "side"},
    "soda": {"price": 1.50, "category": "drink"},
    "salad": {"price": 4.00, "category": "side"}
}

# print full menu (one line per item)
print("Menu:")
for item_name in menu:
    # pulling the price from the nested dict
    price = menu[item_name]["price"]
    category = menu[item_name]["category"]
    print(f"{item_name} (${price:.2f}) - {category}")

# order should be a list of dicts
order = []

# ask how many different items they want to order
num_items = int(input("How many different items do you want to order? "))

# loop that many times and collect item/qty
for i in range(num_items):
    name = input("Item name: ")
    qty = int(input("Quantity: "))

    # store each choice as a dict inside the list
    order.append({"item": name, "qty": qty})

# now compute bill
total = 0.0  

print("\nOrder:")

for entry in order: # grab what user typed for item and qty
    item = entry["item"]
    qty = entry["qty"]

    # check if item exists in menu dictionary
    if item in menu:
        price = menu[item]["price"] # pull

        line_total = price * qty # compute line total

        total += line_total # add to total

        # print line in required format style
        print(f"{item} x{qty} @ ${price:.2f} = ${line_total:.2f}")
    else: # if not on menu, warn and skip it
        print(f"Item '{item}' not on menu, skipping.")

print("--------------")
print(f"Total: ${total:.2f}")
