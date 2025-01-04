class Book:
    def __init__(self, title, author, year, genre, copies, waiting_list=None, is_popular=False):
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.copies = copies
        self.available_copies = copies
        self.waiting_list = waiting_list if waiting_list else []  # List of usernames
        self.is_popular = is_popular  # Boolean indicating if the book is popular

    def __str__(self):
        return (f"Book({self.title}, {self.author}, {self.year}, {self.genre}, "
                f"Copies: {self.copies}, Available: {self.available_copies}, "
                f"Popular: {self.is_popular}, Waiting List: {self.waiting_list})")

    def borrow_book(self, username):
        if self.available_copies > 0:
            self.available_copies -= 1
            return True
        else:
            if username not in self.waiting_list:
                self.waiting_list.append(username)
            return False


    def return_book(self):
        if self.available_copies < self.copies:
            self.available_copies += 1
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
            "waiting_list": ",".join(self.waiting_list),  # Convert list to string for CSV
            "is_popular": str(self.is_popular).lower()  # Convert boolean to string for CSV
        }

    @classmethod
    def from_dict(cls, data):
        """
        Creates a Book object from a dictionary, with default values for missing keys.
        """
        waiting_list = data.get("waiting_list", "").split(",") if data.get("waiting_list") else []
        return cls(
            data["title"],
            data["author"],
            int(data["year"]),
            data["genre"],
            int(data["copies"]),
            waiting_list,
            is_popular=False  # Default to False since this field is irrelevant here
        )

