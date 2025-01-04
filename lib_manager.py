from file_utils import load_books, save_books

import csv

def load_popular_books_with_waiting_list(filename="popular_books.csv"):
    try:
        with open(filename, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            books = []
            for row in reader:
                row["waiting_list"] = [user.strip() for user in row["waiting_list"].split(",")] if row["waiting_list"] else []
                books.append(row)
            return books
    except FileNotFoundError:
        return []  # Return an empty list if the file doesn't exist


def save_popular_books_with_waiting_list(popular_books, filename="popular_books.csv"):
    """
    Saves popular books and their waiting lists to a CSV file.
    """
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = ["title", "waiting_list"]
        writer = csv.DictWriter(file, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)  # Use minimal quoting
        writer.writeheader()
        for book in popular_books:
            # Convert the waiting list back to a comma-separated string
            book["waiting_list"] = ",".join(book["waiting_list"])
            writer.writerow(book)


def add_to_waiting_list(popular_filename, title, username):
    """
    Adds a user to the waiting list of a popular book.
    """
    books = load_books("books.csv")
    for book in books:
        if book.title.strip().lower() == title.strip().lower() and book.available_copies > 0:
            print(f"Copies are available for '{title}'. No need to join the waiting list.")
            return
    popular_books = load_popular_books_with_waiting_list(popular_filename)
    for book in popular_books:
        if book["title"].strip().lower() == title.strip().lower():
            if username not in book["waiting_list"]:
                book["waiting_list"].append(username)
                save_popular_books_with_waiting_list(popular_books, popular_filename)
                print(f"User '{username}' added to the waiting list for '{title}'.")
                return
            else:
                print(f"User '{username}' is already on the waiting list for '{title}'.")
                return
    print(f"Book '{title}' not found in the popular books list.")

def add_to_regular_waiting_list(book_filename, title, username):
    """
    Adds a user to the waiting list of a regular book.
    """
    books = load_books(book_filename)
    for book in books:
        if book.title.strip().lower() == title.strip().lower():
            if username in book.waiting_list:
                print(f"User '{username}' is already on the waiting list for '{title}'.")
                return
            if book.available_copies > 0:
                print(f"Copies are available for '{title}'. No need to join the waiting list.")
                return
            book.waiting_list.append(username)
            save_books(book_filename, books)
            print(f"User '{username}' added to the waiting list for '{title}'.")
            return
    print(f"Book '{title}' not found in the library.")

def show_all_waiting_lists(book_filename, popular_filename):
    """
    Displays all waiting lists for both regular and popular books.
    """
    print("\nRegular Waiting Lists:")
    regular_waiting_lists = get_regular_waiting_list(book_filename)
    for title, waiting_list in regular_waiting_lists.items():
        if waiting_list:
            print(f"'{title}': {waiting_list}")

    print("\nPopular Waiting Lists:")
    popular_books = load_popular_books_with_waiting_list(popular_filename)
    for book in popular_books:
        if book["waiting_list"]:
            print(f"'{book['title']}': {book['waiting_list']}")




def remove_from_waiting_list(popular_filename, title):
    """
    Removes the first user from the waiting list of a popular book.
    """
    popular_books = load_popular_books_with_waiting_list(popular_filename)
    for book in popular_books:
        if book["title"].strip().lower() == title.strip().lower():
            if book["waiting_list"]:
                removed_user = book["waiting_list"].pop(0)  # Remove the first user
                save_popular_books_with_waiting_list(popular_books, popular_filename)
                print(f"User '{removed_user}' removed from the waiting list for '{title}'.")
                return removed_user
            else:
                print(f"No users are on the waiting list for '{title}'.")
                return None
    print(f"Book '{title}' not found in the popular books list.")
    return None

def get_popular_waiting_list(popular_filename):
    """
    Returns the waiting list of each popular book in the library.
    """
    popular_books = load_popular_books_with_waiting_list(popular_filename)
    waiting_lists = {}
    for book in popular_books:
        waiting_lists[book["title"]] = book["waiting_list"]
    return waiting_lists


def get_regular_waiting_list(book_filename):
    """
    Returns the waiting list of each regular book in the library.
    """
    books = load_books(book_filename)
    waiting_lists = {}
    for book in books:
        waiting_lists[book.title] = book.waiting_list
    return waiting_lists


def get_waiting_list_count(popular_filename, title):
    """
    Returns the number of users on the waiting list for a popular book.
    """
    popular_books = load_popular_books_with_waiting_list(popular_filename)
    for book in popular_books:
        if book["title"].strip().lower() == title.strip().lower():
            return len(book["waiting_list"])
    print(f"Book '{title}' not found in the popular books list.")
    return 0

def borrow_popular_book(book_filename, popular_filename, title, username):
    """
    Allows a user to borrow a popular book if the waiting list is empty.
    If the waiting list is not empty, adds the user to the waiting list.
    """
    # Check if the book is popular
    waiting_list_count = get_waiting_list_count(popular_filename, title)

    if waiting_list_count > 0:
        # Add user to waiting list if the book is not immediately available
        add_to_waiting_list(popular_filename, title, username)
        print(f"'{title}' is currently unavailable. User '{username}' added to the waiting list.")
        return

    # Borrow the book from the main library
    books = load_books(book_filename)
    for book in books:
        if book.title.strip().lower() == title.strip().lower():
            if book.borrow_book(username):
                print(f"Book '{title}' borrowed successfully by '{username}'.")
                save_books(book_filename, books)
                return
            else:
                print(f"Book '{title}' is not available for borrowing.")
                return
    print(f"Book '{title}' not found in the library.")




def borrow_book(book_filename, popular_filename, title, username):
    """
    Allows a user to borrow a book, considering its popularity.
    If the book is popular and unavailable, adds the user to its waiting list.
    """
    books = load_books(book_filename)
    popular_books = load_popular_books_with_waiting_list(popular_filename)

    for book in books:
        if book.title.lower() == title.lower():
            if title in popular_books:
                print(f"'{title}' is a popular book!")
            if book.borrow_book(username):
                print(f"Book '{title}' borrowed successfully by {username}.")
                book.copies -=1
            else:
                print(f"No copies available. {username} added to the waiting list for '{title}'.")
            save_books(book_filename, books)  # Save updated book data
            return
    print(f"Book '{title}' not found.")


def show_popular_books(popular_filename):
    """
    Displays the list of popular books.
    """
    popular_books = load_popular_books_with_waiting_list(popular_filename)
    print("Popular Books:")
    for book in popular_books:
        print(book)


def mark_as_popular(book_filename, popular_filename, title):
    """
    Marks a book as popular by adding it to the popular books file.
    """
    books = load_books(book_filename)
    popular_books = load_popular_books_with_waiting_list(popular_filename)

    for book in books:
        if book.title.strip().lower() == title.strip().lower():
            for popular_book in popular_books:
                if popular_book["title"].strip().lower() == title.strip().lower():
                    print(f"Book '{title}' is already marked as popular.")
                    return

            popular_books.append({"title": title, "waiting_list": []})
            save_popular_books_with_waiting_list(popular_books, popular_filename)
            print(f"Book '{title}' marked as popular.")
            return

    print(f"Book '{title}' not found in the library.")


