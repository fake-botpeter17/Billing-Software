# Imports
from tkinter.filedialog import askopenfilename
from typing import Generator
from pymongo import MongoClient
from urllib.parse import quote_plus
from tkinter import Tk, Frame, Label, Entry, Button, messagebox
from PyQt6.QtWidgets import (
    QTableWidget,
    QMainWindow,
    QApplication,
    QTableWidgetItem,
    QMessageBox,
)
from PyQt6.QtGui import QIcon
from PyQt6 import uic
from PyQt6.QtCore import Qt
from bcrypt import hashpw
from pickle import load
from datetime import datetime, date
from urllib import request
from os import getenv as cred_
from sys import exit as exi
from atexit import register as exit_manager

# Global Declaration of Column Position
Name_Col, Rate_Col, ID_Col, Qnty_Col, Disc_prcnt_Col, Disc_Col, Price_Col = 2,3,1,4,5,6,7

# Global Variables
Admin = False  # Used for Authentication and permissions
Name = str()  # Name of the User
logging_out = False
Designation = None
User = str()  # Stores the current user info
bill_data = dict()  # Stores data as {Item_ID : Row} Acts as temp for Current Bill items

def cred(attr :str, parse :bool = False) -> str | None:
    """Returns the value of the environment variable with the given name."""
    if not parse:
        return cred_(attr)
    env = cred_(attr)
    if env is not None:
        return quote_plus(env)
    return None

def Init() -> None:
    try:
        global client, db
        url = cred("Mongo_Con_Str")
        if url is None:
            raise ValueError("URL")
        print(eval(url))
        print(quote_plus(eval(url)))
        client = MongoClient(quote_plus(eval(url)))
        db_name = cred("Mongo_DB")
        if db_name is None:
            raise ValueError("DB")
        db = client[db_name]
    except ValueError as ve:
        reason = ve.args
        if reason == "URL":
            messagebox.showerror("Error", "Server Authentication Failure! Contact Admin")
        elif reason == "DB":
            messagebox.showerror("Error", "Database Authentication Failure! Contact Admin")
        exit(True)
    global Admin
    Admin = False
    Login()

def Login() -> None:
    global login_window
    #Initialization
    login_window = Tk()
    frame = Frame(bg="#333333")
    login_window.title("Login")
    login_window.geometry("550x600")
    login_window.configure(bg="#333333")
    #Widgets
    login_label = Label(frame, text="Login", font=("Helvetica", 30), bg="#333333", fg="#FF3399", pady=40)
    username_label = Label(frame, text="Username: ", font=("Helvetica", 15), bg="#333333", fg="#FFFFFF")
    password_label = Label(frame, text="Password: ", font=("Helvetica", 15), bg="#333333", fg="#FFFFFF")
    #Inputs
    username_entry = Entry(frame, font=("Helvetica", 15))
    password_entry = Entry(frame, show="*", font=("Helvetica", 15))
    #Login_Button
    login_button = Button(
        frame,
        text="Login",
        command=lambda: Auth(username_entry.get(), password_entry.get()),
        bg="#ffffff",
        fg="#FF3399",
    )
    login_window.bind("<Return>", lambda event: ValidateEntry())
    #Layout
    login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
    username_label.grid(row=1, column=0)
    username_entry.grid(row=1, column=1, pady=20)
    password_label.grid(row=2, column=0)
    password_entry.grid(row=2, column=1, pady=20)
    login_button.grid(row=3, column=0, columnspan=2, pady=30)
    #Checking_Input
    def ValidateEntry() -> None:
        if username_entry.get() and password_entry.get():
            login_button.invoke()
        elif (len(username_entry.get()) == 0) and (len(password_entry.get()) == 0):
            messagebox.showerror(
                title="Authentication Error!",
                message="Enter the Username and Password!",
            )
        elif len(username_entry.get()) == 0:
            messagebox.showerror(
                title="Authentication Error!", 
                message="Enter the Username!"
            )
        elif len(password_entry.get()) == 0:
            messagebox.showerror(
                title="Authentication Error!", 
                message="Enter the Password!"
            )
        else: return
    #Final
    frame.pack()
    login_window.mainloop()
#Authentication
def Auth(user :str, pwd :str) -> None:
    global db
    users_table = db['users']
    result = users_table.find_one({'uid':user},{'uid':False})
    if result is None:
        messagebox.showerror(title="Authentication Error!", message="Invalid Username! Try Again!")
        return 
    try:
        with open("BillingInfo.dat",'rb+') as f:
           data = load(f)
    except FileNotFoundError:
        messagebox.showerror(title="Application Error", message="abms.dll is missing! Contact Admin")
        exit(True)
    salt = data[result['salt']]
    password = hashpw(pwd.encode(), salt)
    #Comparing Hashed Passwords
    if str(password) == result['hashed_pwd']:  
        global Designation, Name
        Designation = result['designation'].title()
        Name = result['name']
        if Designation.casefold() == "Admin".casefold():
            global Admin
            Admin = True 
            messagebox.showinfo(
                title="Login Successful!", message="You are now logged in as Admin."
            )
        else:
            messagebox.showinfo(
                title="Login Successful!", message="You are now logged in."
            )
        global User
        User = user
        login_window.destroy()  # Closing the Login Window after successful Login
        #main()  

    else:
        messagebox.showerror(
            title="Authentication Error!", message="Wrong Username or Password"
        )
if __name__ == '__main__':
    Init()