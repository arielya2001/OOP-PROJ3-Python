from werkzeug.security import check_password_hash

from Book import BookFactory
from user import User
from file_utils import load_data, save_data

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
    user_file = "users.csv"

    register_user(user_file, "john_doe", "securepassword123")
    authenticate_user(user_file, "john_doe", "securepassword123")
