import csv
from Book import Book

def load_data(filename):
    """reads data from csv, and make a list of dict for me!
        each element has key and value"""
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file) #reads! each col to key and each data in it to value of that row!
            data = []
            for row in reader: #for each element in reader(which is dict) add it to the lst. each row.
                data.append(row) #adding each row to the lst. adding dicts.
            return data
    except FileNotFoundError:
        return []

def save_data(filename, data, fieldnames):
    """Writes data to csv.
        filednames = we have to store the keys(col) in this list.
        data = the actual list of dicts.
        filename = name of the file we want to save to."""
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames) #allowing us to write. fieldnames = col names. the keys.
        writer.writeheader() #writes the columns headers in the file. the keys of the dict.
        writer.writerows(data) #writes the rows headers in the file. the values of the dict.

def load_books(filename):
    books = []
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                books.append(Book.from_dict(row))
    except FileNotFoundError:
        pass
    return books

def save_books(filename, books):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ["title", "author", "is_loaned", "copies", "genre", "year"]  # Match books.csv
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for book in books:
            writer.writerow({
                "title": book.title,
                "author": book.author,
                "is_loaned": book.is_loaned,
                "copies": book.copies,
                "genre": book.genre,
                "year": book.year
            })

def find_book_by_title(data, title):
    for book in data:
        if book["title"].strip().lower() == title.strip().lower():
            return book
    return None


