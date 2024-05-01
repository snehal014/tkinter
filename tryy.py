import tkinter as tk
from tkinter import *
from tkinter import messagebox
import mysql.connector as m
import hashlib
from tkinter import ttk

# Establish database connection
mydatabase = m.connect(host="localhost", user="root", password="jklm@me@021", database="users")
login_query = "SELECT * FROM users WHERE username = %s AND password = %s"

def hash_password(password):
    """Hash the password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def clear_entry(*entries):
    for entry in entries:
        entry.delete(0,'end')
def register_user():
    username = username_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    # Validate input fields
    if not username or not email or not password:
        messagebox.showerror("Error", "Please fill in all fields")
        return None

    try:
        # Hash the password
        hashed_password = hash_password(password)

        # Insert data into database
        cursor = mydatabase.cursor()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, hashed_password))
        mydatabase.commit()  # Commit the changes to the database

        messagebox.showinfo("Registration Successful", "User registered successfully!")
    except m.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
    clear_entry(username_entry,email_entry,password_entry)
def login_user():
    username = login_username_entry.get()
    password = login_password_entry.get()

    if not username or not password:
        messagebox.showerror("Error", "Please enter username and password")
        return

    try:
        # Hash the entered password for comparison
        hashed_password = hash_password(password)

        # Check if user exists with the provided credentials
        cursor = mydatabase.cursor()
        cursor.execute(login_query, (username, hashed_password))
        user = cursor.fetchone()

        if user:
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            # Close the login window or perform other actions upon successful login
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
    except m.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")

def open_login_window():
    # Create login window
    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.geometry('300x200')

    # Create labels and entry widgets for login form
    tk.Label(login_window, text="Username:").pack(pady=5)
    global login_username_entry
    login_username_entry = tk.Entry(login_window, width=30)
    login_username_entry.pack(pady=5)

    tk.Label(login_window, text="Password:").pack(pady=5)
    global login_password_entry
    login_password_entry = tk.Entry(login_window, width=30, show="*")
    login_password_entry.pack(pady=5)

    # Create login button within the login window
    login_button = tk.Button(login_window, text="Login", command=login_user)
    login_button.pack(pady=10)

def display_registered_users():
    # Retrieve registered users from the database
    try:
        cursor = mydatabase.cursor()
        cursor.execute("SELECT username, email FROM users")
        users = cursor.fetchall()

        # Clear existing items in the Treeview
        for item in users_tree.get_children():
            users_tree.delete(item)

        # Insert users data into the Treeview
        for user in users:
            users_tree.insert("", "end", values=user)
    except m.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")

def data_window():
    data_show_window = tk.Toplevel(root)
    data_show_window.title("Registered Users")
    data_show_window.geometry('600x400')

    # Create a Treeview widget to display registered users
    global users_tree
    users_tree = ttk.Treeview(data_show_window, columns=("Username", "Email"), show="headings")
    users_tree.heading("Username", text="Username")
    users_tree.heading("Email", text="Email")
    users_tree.pack(fill="both", expand=True)

    # Display registered users
    display_registered_users()

    # Create a button to close the window
    close_button = tk.Button(data_show_window, text="Close", command=data_show_window.destroy)
    close_button.pack(pady=10)

# Create main window
root = tk.Tk()
root.geometry('600x400')
root.title("User Authentication")

# Create labels and entry widgets for registration form
tk.Label(root, text="Username:").pack(pady=5)
username_entry = tk.Entry(root, width=30)
username_entry.pack(pady=5)

tk.Label(root, text="Email:").pack(pady=5)
email_entry = tk.Entry(root, width=30)
email_entry.pack(pady=5)

tk.Label(root, text="Password:").pack(pady=5)
password_entry = tk.Entry(root, width=30, show="*")
password_entry.pack(pady=5)

# Create register and open login buttons
register_button = tk.Button(root, text="Register", command=register_user)
register_button.pack(pady=10)

open_login_button = tk.Button(root, text="Login", command=open_login_window)
open_login_button.pack(pady=5)

# Create a button to view registered users
view_entry_button = tk.Button(root, text="View Entry", command=data_window)
view_entry_button.pack(pady=5)

cl=tk.Button(root,text="Clear",command=lambda:clear_entry(username_entry,email_entry,password_entry))
cl.pack(pady=5)
# Run the main event loop
root.mainloop()

#
