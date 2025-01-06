from file_utils import load_books, save_books, load_data, find_book_by_title, save_data
from collections import Counter

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
def add_to_waiting_list(popular_filename, title, username):
    books = load_books("books.csv")
    for book in books:
        if book.title.strip().lower() == title.strip().lower():
            if book.available_copies > 0:
                print(f"Copies are available for '{title}'. No need to join the waiting list.")
                return
            # Increment request count
            book.request_count += 1
            save_books("books.csv", books)  # Save updated request counts
            break

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
def update_available_books(book_filename, available_books_filename):
    books = load_books(book_filename)
    available_books = [book for book in books if book.available_copies > 0]
    with open(available_books_filename, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = ["title", "author", "genre", "year", "available_copies"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for book in available_books:
            writer.writerow({
                "title": book.title,
                "author": book.author,
                "genre": book.genre,
                "year": book.year,
                "available_copies": book.available_copies
            })

def update_loaned_books(book_filename, loaned_books_filename):
    books = load_books(book_filename)
    loaned_books = [book for book in books if book.available_copies < book.copies]
    with open(loaned_books_filename, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = ["title", "author", "genre", "year", "loaned_copies"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for book in loaned_books:
            loaned_copies = book.copies - book.available_copies
            writer.writerow({
                "title": book.title,
                "author": book.author,
                "genre": book.genre,
                "year": book.year,
                "loaned_copies": loaned_copies
            })




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


def update_available_and_loaned_books(books):
    available_books = [book.to_dict() for book in books if not book.is_loaned]
    loaned_books = [book.to_dict() for book in books if book.is_loaned]
    save_data("available_books.csv", available_books, fieldnames=["title", "author", "copies", "genre", "year"])
    save_data("loaned_books.csv", loaned_books, fieldnames=["title", "author", "copies", "genre", "year"])


def borrow_book(book_filename, popular_filename, title, username):
    """
    Allows a user to borrow a book, considering its popularity.
    If the book is popular and unavailable, adds the user to its waiting list.
    """
    books = load_books(book_filename)

    for book in books:
        if book.title.strip().lower() == title.strip().lower():
            if book.borrow_book(username):
                print(f"Book '{title}' borrowed successfully by {username}.")
            else:
                print(f"No copies available. {username} added to the waiting list for '{title}'.")
            save_books(book_filename, books)  # Save updated book data
            update_available_and_loaned_books(books)  # Update available and loaned books
            return
    print(f"Book '{title}' not found.")

def return_book(book_filename, available_filename, loaned_filename, title, username):
    """
    Return a book, updating available_books.csv and loaned_books.csv.
    """
    available_books = load_data(available_filename)
    loaned_books = load_data(loaned_filename)
    all_books = load_data(book_filename)

    # Find the book in loaned_books
    book = find_book_by_title(loaned_books, title)
    if book and book.get("borrowed_by") == username:
        # Remove from loaned_books and add to available_books
        loaned_books.remove(book)
        del book["borrowed_by"]
        available_books.append(book)

        # Update is_loaned if necessary
        book_in_all_books = find_book_by_title(all_books, title)
        if book_in_all_books:
            book_in_all_books["is_loaned"] = "No"

        save_data(available_filename, available_books, fieldnames=list(available_books[0].keys()))
        save_data(loaned_filename, loaned_books, fieldnames=list(loaned_books[0].keys()))
        print(f"Book '{title}' returned successfully by {username}.")
    else:
        print(f"Book '{title}' not found in the loaned books or not borrowed by {username}.")

def update_popularity(popular_filename, title):
    """
    Update the popularity count for a book in the popular_books.csv file.
    """
    popular_books = load_data(popular_filename)
    book = find_book_by_title(popular_books, title)

    if book:
        book["popularity_count"] = str(int(book["popularity_count"]) + 1)
    else:
        popular_books.append({"title": title, "popularity_count": "1"})

    save_data(popular_filename, popular_books, fieldnames=["title", "popularity_count"])

def get_top_10_popular_books(popular_filename):
    """
    Returns the top 10 most popular books based on their waiting list size.
    """
    popular_books = load_popular_books_with_waiting_list(popular_filename)
    # Calculate popularity score dynamically as the length of the waiting list
    popularity_scores = [
        {"title": book["title"], "popularity_score": len(book["waiting_list"])}
        for book in popular_books
    ]
    # Sort by popularity score in descending order
    popularity_scores.sort(key=lambda x: x["popularity_score"], reverse=True)
    # Return the top 10 most popular books
    return popularity_scores[:10]


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


