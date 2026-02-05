def days_overdue(due_date, today):
    # Return days overdue (negative means not overdue yet)
    # example: due_date=20, today=24 -> 4 days overdue
    return today - due_date


def format_status(book):
    # book is a dictionary like:
    # {"title": "...", "status": "...", "due_date": 20, "today": 24}
    # we return a single formatted string line for this book

    title = book["title"]
    status = book["status"]

    # if available, no due date needed in output
    if status == "available":
        return f"\"{title}\" (available)"

    # checked out: could be overdue or not, so we check due_date vs today
    elif status == "checked_out":
        due = book["due_date"]
        today = book["today"]

        overdue_days = days_overdue(due, today)

        # if overdue_days is positive then it is overdue
        if overdue_days > 0:
            return f"\"{title}\" (checked out, due Jan {due}: {overdue_days} days overdue)"
        else:
            # not overdue yet (could be 0 or negative)
            return f"\"{title}\" (checked out)"

    # overdue status (if they marked it overdue in data)
    elif status == "overdue":
        due = book["due_date"]
        today = book["today"]

        overdue_days = days_overdue(due, today)

        # if it says overdue, we print it overdue
        return f"\"{title}\" (overdue, due Jan {due}: {overdue_days} days overdue)"

    # if status is something unexpected, still return something readable
    else:
        return f"\"{title}\" (unknown status)"


def print_inventory(inventory):
    # inventory is a list of book dictionaries
    # this function prints every book line using format_status()

    for book in inventory:
        print(format_status(book))
