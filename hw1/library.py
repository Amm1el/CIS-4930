def days_overdue(due_date, today):
    return today - due_date

def format_status(book):
    if book["status"] == "available":
        return f"\"{book['title']}\" (available)"
    elif book["status"] == "checked_out":
        overdue = days_overdue(book["due_date"], book["today"])
        if overdue > 0:
            return f"\"{book['title']}\" (checked out, due Jan {book['due_date']}: {overdue} days overdue)"
        else:
            return f"\"{book['title']}\" (checked out)"
    else:
        return f"\"{book['title']}\" (overdue)"

def print_inventory(inventory):
    for book in inventory:
        print(format_status(book))
