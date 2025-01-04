class Book:
    def __init__(self, title, author, year, genre, copies):
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.copies = copies
        self.available_copies = copies

    def __str__(self):
        return f"Book({self.title}, {self.author}, {self.year}, {self.genre}, Copies: {self.copies})"

class BookFactory:
    @staticmethod
    def create_book(genre, title, author, year, copies):
        return Book(title, author, year, genre, copies)
