from werkzeug.security import check_password_hash

from user import User
from file_utils import load_data, save_data
from lib_manager import show_popular_books, add_to_waiting_list, borrow_popular_book, mark_as_popular, \
    get_waiting_list_count, remove_from_waiting_list, get_regular_waiting_list, add_to_regular_waiting_list, \
    show_all_waiting_lists, borrow_book


def register_user(filename, username, password):
    users = load_data(filename)
    for user in users:
        if user["username"] == username:
            print(f"Error: Username '{username}' already exists.")
            return False
    password_hash = User.hash_password(password)
    users.append({"username": username, "password_hash": password_hash})
    save_data(filename, users, ["username", "password_hash"])
    print(f"User '{username}' registered successfully.")
    return True

def authenticate_user(filename, username, password):
    users = load_data(filename)
    for user in users:
        if user["username"] == username:
            if check_password_hash(user["password_hash"], password):
                print(f"Login successful for user '{username}'.")
                return True
            else:
                print("Error: Incorrect password.")
                return False
    print("Error: Username not found.")
    return False

if __name__ == "__main__":
    # Example usage

    # user_file = "users.csv"
    #
    # register_user(user_file, "john_doe", "securepassword123")
    # authenticate_user(user_file, "john_doe", "securepassword123")

    book_filename = "books.csv"
    popular_filename = "popular_books.csv"

    # Mark a book as popular
    #mark_as_popular("books.csv", "popular_books.csv", "The Great Gatsby")

    # Borrow a book
    #add_to_waiting_list("popular_books.csv", "1984", "charlie")

    #count = get_waiting_list_count("popular_books.csv", "1984")
    #print(f"Users waiting for '1984': {count}")

    #borrow_popular_book("books.csv", "popular_books.csv", "1984", "david")

    #remove_from_waiting_list("popular_books.csv", "1984")

    # Show popular books
    borrow_book("books.csv", "popular_books.csv", "Moby Dick", "john_doe")
    add_to_regular_waiting_list("books.csv", "Moby Dick", "bigger")

    show_all_waiting_lists("books.csv", "popular_books.csv")


