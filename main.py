# Simulate borrowing requests for books
from file_utils import save_books, load_books, load_data, save_data

def update_popular_books(book_filename, popular_filename):
    """
    Updates the popular_books.csv file with the top 10 most popular books based on request count.
    """
    # Load all books
    books = load_books(book_filename)

    # Sort books by request_count in descending order and select the top 10
    top_10_books = sorted(books, key=lambda book: book.request_count, reverse=True)[:10]

    # Prepare data for popular_books.csv
    popular_books = [
        {
            "title": book.title,
            "waiting_list": ",".join(book.waiting_list)  # Convert waiting list to CSV-compatible string
        }
        for book in top_10_books
    ]

    # Save popular books to popular_books.csv
    save_data(popular_filename, popular_books, fieldnames=["title", "waiting_list"])

    # Print results for verification
    print(f"Popular books updated in {popular_filename}:")
    for book in popular_books:
        print(book)


def simulate_requests(book_filename, titles, usernames):
    """
    Simulate borrow requests to increase request_count for specified books.
    """
    books = load_books(book_filename)
    for title, username in zip(titles, usernames):
        for book in books:
            if book.title.strip().lower() == title.strip().lower():
                if book.available_copies > 0:
                    book.borrow_book(username)
                    print(f"'{book.title}' borrowed by {username}. Remaining copies: {book.available_copies}.")
                else:
                    book.request_count += 1
                    print(f"Request count increased for '{book.title}'. Current count: {book.request_count}")
                break
    save_books(book_filename, books)  # Save updated request counts


# Main Code Execution
if __name__ == "__main__":
    books_filename = "books.csv"
    popular_books_filename = "popular_books.csv"

    # Titles and usernames to simulate requests for
    titles_to_request = [
        "The Odyssey",
        "Jane Eyre",
        "Harry Potter and the Philosopher's Stone",
        "Beloved",
        "Slaughterhouse-Five"
    ]
    usernames = ["user_a", "user_b", "user_c", "user_d", "user_e"]

    # Simulate requests
    simulate_requests(books_filename, titles_to_request, usernames)

    # Update popular books
    update_popular_books(books_filename, popular_books_filename)

    # Verify updated popular books
    print("\nUpdated Popular Books:")
    popular_books = load_data(popular_books_filename)
    for book in popular_books:
        print(book)
