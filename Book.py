class Book:
    def __init__(self, title, author, year, genre, copies, waiting_list=None, request_count=0):
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.copies = copies
        self.available_copies = copies
        self.is_loaned = "Yes" if self.available_copies == 0 else "No"  # Initialize based on available_copies
        self.waiting_list = waiting_list if waiting_list else []  # List of usernames
        self.request_count = request_count  # Track how often the book is requested

    def __str__(self):
        return (f"Book({self.title}, {self.author}, {self.year}, {self.genre}, "
                f"Copies: {self.copies}, Available: {self.available_copies}, "
                f"Loaned: {self.is_loaned}, Waiting List: {self.waiting_list}, Request Count: {self.request_count})")

    def borrow_book(self, username):
        if self.available_copies > 0:
            self.available_copies -= 1
            self.is_loaned = "Yes" if self.available_copies == 0 else "No"
            print(f"Book '{self.title}' borrowed. Remaining copies: {self.available_copies}.")
            return True
        else:
            if username not in self.waiting_list:
                self.waiting_list.append(username)
                print(f"User '{username}' added to waiting list for '{self.title}'.")
            return False

    def return_book(self):
        if self.available_copies < self.copies:
            self.available_copies += 1
            self.is_loaned = "Yes" if self.available_copies == 0 else "No"  # Update loaned status
            if self.waiting_list:
                next_user = self.waiting_list.pop(0)
                print(f"Book '{self.title}' assigned to {next_user} from the waiting list.")
            return True
        return False

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "genre": self.genre,
            "copies": self.copies,
            "available_copies": self.available_copies,
            "is_loaned": self.is_loaned,  # Store as "Yes" or "No"
            "waiting_list": ",".join(self.waiting_list),
            "request_count": self.request_count  # Include request_count
        }

    @classmethod
    def from_dict(cls, data):
        waiting_list = data.get("waiting_list", "").split(",") if data.get("waiting_list") else []
        book = cls(
            data["title"],
            data["author"],
            int(data["year"]),
            data["genre"],
            int(data["copies"]),
            waiting_list,
            request_count=int(data.get("request_count", 0))
        )
        book.available_copies = int(data.get("available_copies", book.copies))
        book.is_loaned = data.get("is_loaned", "No")  # Initialize from CSV
        return book
