"""
CIS-4930 Introduction to Python, Spring 2026
Homework : 3
Problem : 2
Student Name: Ammiel Bowen
Student ID: ab22dv
Section: 0003
Submission Date: 03-01-2026
"""

# built-ins only type of assignment
# in, .index style scanning, sorted(), sort(), key=
# also comments for big O required

# sample data given
sales = [
    {"title": "Python Tricks", "price": 30.0, "genre": "Programming", "copies": 2},
    {"title": "Gardening 101", "price": 18.5, "genre": "Hobby", "copies": 1},
    {"title": "Deep Learning", "price": 45.0, "genre": "Programming", "copies": 1},
    {"title": "Time Management", "price": 22.0, "genre": "Self-help", "copies": 3},
    {"title": "Fluent Python", "price": 40.0, "genre": "Programming", "copies": 1},
]


def was_sold(sales, title):
    # time complexity: O(n) worst-case because we may scan every sale entry once
    # n = len(sales)
    for entry in sales:
        if entry["title"] == title:
            return True
    return False


def find_first_by_genre(sales, genre):
    # worst-case time complexity: O(n), scan list once until we find it (or dont)
    # no extra data structures, just direct scan (index but w condition)
    i = 0
    while i < len(sales):
        if sales[i]["genre"] == genre:
            return i
        i += 1
    return -1


def revenue_sorted(sales):
    # sorted() returns  NEW list so original is unchanged (required)
    # sorting complexity is O(n log n)
    # key function is O(1) per element, so overall still O(n log n)

    # sort by:
    # 1) revenue descending (price*copies)
    # 2) tie -> alphabetical title ascending
    return sorted(
        sales,
        key=lambda x: (-(x["price"] * x["copies"]), x["title"])
    )


def unique_genres(sales):
    # use a set for fast checking
    # set membership is ~O(1) average, so repeated checks are efficient

    seen = set()  # fast "have we seen this genre already"
    for entry in sales:
        g = entry["genre"]
        if g not in seen:
            seen.add(g)

    # convert to sorted list alphabetically
    # building set: O(n)
    # sorting unique genres: O(k log k) where k = number of unique genres
    # total: O(n + k log k)
    return sorted(list(seen))

'''
Part 5 scale analysis (comments only)
If was_sold() is called once with 100,000 entries, O(n) might still be acceptable
because 100k comparisons is not insane for a single call.
BUT if owner calls was_sold() thousands of times per day, then O(n) repeated becomes O(n*m)
which is huge. Design change: build a set or dict of titles once (preprocessing),
then lookups become ~O(1) average per query instead of scanning every time.
'''

# tests (expected)
print(was_sold(sales, "Python Tricks"))              # True
print(find_first_by_genre(sales, "Programming"))     # 0
print(unique_genres(sales))                          # ['Hobby', 'Programming', 'Self-help']

# show the revenue ranking output too (not required exact formatting)
ranked = revenue_sorted(sales)
for r in ranked:
    rev = r["price"] * r["copies"]
    print(r["title"], rev)