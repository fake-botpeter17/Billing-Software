# Imports
import string
from os import path
from threading import Thread
from typing import LiteralString
from requests import post
from win32api import ShellExecute
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from pathlib import Path
from pyautogui import press
from tkinter.filedialog import askopenfilename
from collections.abc import Generator
from tkinter import Tk, Frame, Label, Entry, Button, messagebox
from PyQt6.QtWidgets import (
    QLabel,
    QMenu,
    QPushButton,
    QTableWidget,
    QMainWindow,
    QApplication,
    QTableWidgetItem,
    QMessageBox,
)
from PyQt6.QtGui import QIcon
from PyQt6 import uic
from PyQt6.QtCore import Qt
from urllib.request import Request, urlopen
from json import dumps, loads
from datetime import datetime, date
from sys import exit as exi
from qt_helper import BillTableColumn

DIREC = Path(__file__).resolve().parent

#Importing Punctuations for Password Validation
punc : LiteralString = string.punctuation

class User:
    __Name :str = str()
    __Designation :str = str()
    __UID :str = str()
    __Logging_Out :bool = False

    @classmethod
    def update(cls  : "User", uid : str, **kwargs : dict[str, str]) -> None:
        """Sets the current user info"""
        cls.__Name :str = kwargs.get("name")
        cls.__Designation :str = kwargs.get("designation")
        cls.__UID :str = uid

    @classmethod
    def getNameDesignation(cls : "User") -> tuple[str, str]:
        return cls.__Name, cls.__Designation

    @classmethod
    def isAdmin(cls : "User") -> bool:
        '''Checks if the current user is an Admin'''
        return cls.__Designation.casefold() == "Admin".casefold()

    @classmethod
    def isLoggingOut(cls : "User") -> bool:
        return cls.__Logging_Out
    
    @classmethod
    def toggleLoggingOut(cls : "User") -> None:
        cls.__Logging_Out = True
        cls.resetUser()

    @classmethod
    def resetUser(cls : "User") -> None:
        cls.__Name :str = str()
        cls.__Designation :str = str()
        cls.__UID :str = str()

class Bill_:
    __Bill_No_Gen :Generator
    __Bill_No :int
    __Items :dict = dict()
    __Cart :dict = dict()

    @staticmethod
    def __Bill_Number() -> Generator:
        """Retreives the latest Bill Number"""
        req :str = f"{url}/getLastBillNo"
        with urlopen(Request(req)) as res:
            Latest_Bill : int | None = loads(res.read().decode())
        if not Latest_Bill:
            Latest_Bill = 10001
        for Bill_Number in range(Latest_Bill + 1, 100000):
            yield Bill_Number

    @classmethod
    def Init(cls : "Bill_") -> None:
        cls.__Bill_No_Gen = cls.__Bill_Number()
        cls.__Bill_No = next(cls.__Bill_No_Gen)
        Cacher = Thread(target=cls.Items_Cacher)
        Cacher.start()

    @classmethod
    def Get_Bill_No(cls : "Bill_") -> int:
        return cls.__Bill_No

    @staticmethod
    def Get_Date() -> str:
        """Returns the current date."""
        return date.today().strftime("%B %d, %Y")

    @staticmethod
    def Get_Time() -> str:
        """Returns the current time."""
        return datetime.now().time().strftime("%H:%M:%S")
    
    @classmethod
    def Increment_Bill_No(cls : "Bill_") -> None:
        cls.__Bill_No = next(cls.__Bill_No_Gen)

    @classmethod
    def Items_Cacher(cls : "Bill_") -> None:
        req = Request(url + "//get_items")
        with urlopen(req, timeout=15) as response:
            items_cache = loads(response.read().decode())
        if not items_cache:
            return
        for item in items_cache:
            cls.__Items[item["id"]] = item

# Global Variables
bill_data = dict()  # Stores data as {Item_ID : Row} Acts as temp for Current Bill items
Bill_No = int()
items_cache = {}

def get_Api(testing: bool = False) -> str:
    """Returns the API URL for the server"""
    if testing:
        return "http://127.0.0.1:5000"
    from pickle import load

    with open("Resources\\sak.dat", "rb") as file:
        return load(file).decode("utf-32")


url: str = get_Api()


def Init() -> None:
    try:
        if_connected_req = Request(f"{url}//connected")
        with urlopen(if_connected_req) as responsee:
            if loads(responsee.read().decode("utf-8")):
                messagebox.showinfo("Success!", "Connected to the server successfully")
            else:
                messagebox.showerror("Error!", "Failed to connect to the server")
    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")
        exit(True)
    Login()


def Items_Cacher():
    global items_cache
    req = Request(url + "//get_items")
    with urlopen(req, timeout=15) as response:
        items_cache_ = loads(response.read().decode())
    for item in items_cache_:
        items_cache[item["id"]] = item


def main():
    Cacher = Thread(target=Items_Cacher)
    Cacher.start()
    global app
    app = QApplication([])
    window = BMS_Home_GUI()
    window.showMaximized()
    exi(app.exec())


def Bill_Number() -> Generator:
    # Get latest Bill No and save it to the below Variable
    req = f"{url}/getLastBillNo"
    with urlopen(Request(req)) as res:
        Latest_Bill = loads(res.read().decode())
    if Latest_Bill is None:
        Latest_Bill = 10001
    for Bill_Number in range(Latest_Bill + 1, 100000):
        yield Bill_Number


def Login() -> None:
    global login_window
    # Initialization
    login_window = Tk()
    frame = Frame(bg="#333333")
    login_window.title("Login")
    login_window.geometry("550x600")
    login_window.configure(bg="#333333")
    # Widgets
    login_label = Label(
        frame, text="Login", font=("Helvetica", 30), bg="#333333", fg="#FF3399", pady=40
    )
    username_label = Label(
        frame, text="Username: ", font=("Helvetica", 15), bg="#333333", fg="#FFFFFF"
    )
    password_label = Label(
        frame, text="Password: ", font=("Helvetica", 15), bg="#333333", fg="#FFFFFF"
    )
    # Inputs
    username_entry = Entry(frame, font=("Helvetica", 15))
    password_entry = Entry(frame, show="*", font=("Helvetica", 15))
    # Login_Button
    login_button = Button(
        frame,
        text="Login",
        command=lambda: ValidateEntry(),
        bg="#ffffff",
        fg="#FF3399",
    )
    login_window.bind("<Return>", lambda event: ValidateEntry())
    # Layout
    login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
    username_label.grid(row=1, column=0)
    username_entry.grid(row=1, column=1, pady=20)
    password_label.grid(row=2, column=0)
    password_entry.grid(row=2, column=1, pady=20)
    login_button.grid(row=3, column=0, columnspan=2, pady=30)

    # Checking_Input
    def ValidateEntry():
        if ValidateEntry_():
            Auth(username_entry.get(), password_entry.get())

    def ValidInp(val, usr: bool = False):
        if len(val) == 0:
            return False
        if usr:
            return val.isalpha()
        else:
            pw: str = val
            intersect = set(pw).intersection(punc)
            if len(intersect) == 0 or (
                len(intersect) == 1 and ({"_"} == intersect or {"@"} == intersect)
            ):
                return True
            elif len(intersect) < 3:
                if "_" in intersect and "@" in intersect:
                    return True
            return False

    def ValidateEntry_() -> None | bool:
        if ValidInp(username_entry.get(), usr=True) and ValidInp(password_entry.get()):
            return True
        elif (len(username_entry.get()) == 0) and (len(password_entry.get()) == 0):
            messagebox.showerror(
                title="Authentication Error!",
                message="Enter the Username and Password!",
            )
        elif len(username_entry.get()) == 0:
            messagebox.showerror(
                title="Authentication Error!", message="Enter the Username!"
            )
        elif len(password_entry.get()) == 0:
            messagebox.showerror(
                title="Authentication Error!", message="Enter the Password!"
            )
        else:
            messagebox.showerror(
                title="Authentication Error!",
                message="Username or Password must contain only letters and numbers!",
            )

    # Final
    frame.pack()
    login_window.mainloop()


# Authentication
def Auth(user: str, pwd: str) -> None:
    URL = f"{url}//authenticate//{user}//{pwd}"
    req = Request(URL)
    response_ = urlopen(req)
    response = response_.read().decode()
    result = loads(response)
    # Comparing Hashed Passwords
    if result is not None:
        User.update(uid=user, **result)
        Bill_.Init()
        if User.isAdmin():
            messagebox.showinfo(
                title="Login Successful!", message="You are now logged in as Admin."
            )
        else:
            messagebox.showinfo(
                title="Login Successful!", message="You are now logged in."
            )
        login_window.destroy()  # Closing the Login Window after successful Login
        main()
    else:
        messagebox.showerror(
            title="Authentication Error!", message="Wrong Username or Password"
        )

Bill_No_Gen: Generator = Bill_Number()  # Memory Efficient way to generate bill no. successively (Generator Object)


class BMS_Home_GUI(QMainWindow):
    menuSales :QMenu
    menuStock :QMenu
    New_Bill_Tab :QMenu
    Bill_Number_Label :QLabel
    Bill_Date_Label :QLabel
    Billed_By_Label :QLabel
    Bill_Time_Label :QLabel
    actionLogout :QMenu
    actionThemes :QMenu
    Profile :QMenu
    Bill_Table :QTableWidget
    Print_Button :QPushButton
    Net_Discount_Label :QLabel
    Total_Label :QLabel
    Net_Total_Label :QLabel

    def __init__(self):
        """
        Should Set the Column width from code appropriately
        """
        global Bill_No
        Bill_No = next(Bill_No_Gen)
        super(BMS_Home_GUI, self).__init__()
        uic.loadUi("BMS_Home_GUI.ui", self)  
        aspect_ratio = 16 / 9  # aspect ratio
        min_height = 900
        min_width = int(min_height * aspect_ratio)
        self.setMinimumSize(min_width, min_height)
        self.setWindowTitle(f"BMS - {User.getNameDesignation()[0]}")
        icon = QIcon("My_Icon.ico")
        self.setWindowIcon(icon)
        if User.isAdmin():
            self.menuSales.setEnabled(True)  
            self.menuStock.setEnabled(True)  
            self.New_Bill_Tab.setEnabled(True)  # Should Set back to Flase at exit 
        self.show()
        self.setup()
        press("tab")

    def setup(self, init: bool = False):
        global Bill_No
        self.setTheme("Resources/Default.qss")
        self.Bill_Number_Label.setText(  
            "Bill No    : {}".format([Bill_No if not init else next(Bill_No_Gen)][0])
        )
        self.Bill_Date_Label.setText(  
            "Bill Date : {}".format(date.today().strftime("%B %d, %Y"))
        )
        self.Billed_By_Label.setText(  
            "Billed By : {} ({})".format(*User.getNameDesignation())
        )
        self.Bill_Time_Label.setText(  
            "Bill Time : {}".format(datetime.now().time().strftime("%H:%M:%S")) 
        )
        self.actionLogout.triggered.connect(lambda: self.logout())  
        self.actionThemes.triggered.connect(lambda: self.setTheme())  
        self.Profile.triggered.connect(  
            lambda: Profile_(User)  # type:ignore
        )  # Should Change after defining Profile GUI
        self.Bill_Table.setColumnCount(8)  
        self.Bill_Table.setRowCount(26)  
        self.Bill_Table.cellChanged.connect(self.handle_cell_change)  
        self.Print_Button.clicked.connect(self.log_bill)  
        # Setting Column Widths
        # Didn't define the width of price col to allow resizing
        self.Bill_Table.setColumnWidth(0, 100)  
        self.Bill_Table.setColumnWidth(BillTableColumn.Id, 150)  
        self.Bill_Table.setColumnWidth(BillTableColumn.Name, 350)  
        self.Bill_Table.setColumnWidth(BillTableColumn.Rate, 150)  
        self.Bill_Table.setColumnWidth(BillTableColumn.Qnty, 150)  
        self.Bill_Table.setColumnWidth(BillTableColumn.Disc_prcnt, 175)  
        self.Bill_Table.setColumnWidth(BillTableColumn.Disc, 175)  

    def closeEvent(self, event):
        if User.isLoggingOut():
            return
        reply = QMessageBox.question(
            self,
            "Exit?",
            "Are you sure you want to quit?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            User.resetUser()
            event.accept()
        else:
            event.ignore()

    def setTheme(self, path: None | str = None) -> None:
        try:
            if path is None:
                path = askopenfilename(
                    title="Select Theme",
                    initialdir=DIREC,
                    filetypes=(("QSS", "*.qss"),),
                )
        except:
            pass
        try:
            with open(path) as f:
                stylesheet = f.read()
                self.setStyleSheet(stylesheet)
        except:
            pass

    def setBillColumn(self, row: int, column: int, value: str | int | float = ""):
        temp = QTableWidgetItem(str(value))
        temp.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.Bill_Table.setItem(row, column, temp)  

    def setCellTracking(self, mode: bool) -> None:
        if not mode:
            self.Bill_Table.cellChanged.disconnect(self.handle_cell_change)  
            return
        self.Bill_Table.cellChanged.connect(self.handle_cell_change)  

    def getText(self, row: int, column: int) -> str:
        data = self.Bill_Table.item(row, column)  
        if data:
            return data.text()
        return ""

    def resetRow(self, row: int) -> None:
        for col in range(8):
            self.setBillColumn(row, col, "")

    def handle_cell_change(self, row, col):
        if row is not None:
            global bill_data
            if col == BillTableColumn.Id:  
                self.setCellTracking(False)
                try:
                    s = self.getText(row, BillTableColumn.Id)
                    Item_ID = int(s)
                    del s
                    if Item_ID not in bill_data:
                        try:
                            self.setCellTracking(False)
                        except:
                            pass
                        self.setBillColumn(row, BillTableColumn.Id, Item_ID)
                except:  # Convertion Error (str -> int)
                    if (
                        self.Bill_Table.item(row, BillTableColumn.Id).text() == ""  
                        or self.Bill_Table.item(row, BillTableColumn.Id).text()  
                        == None
                    ):
                        self.resetRow(row)
                        tmp: list = list(bill_data.values())
                        if tmp is not None:
                            if row in tmp:
                                ind = tmp.index(row)
                                del bill_data[
                                    list(bill_data.keys())[ind]
                                ]  
                                self.CalcTotal()
                        return

                try:
                    data = items_cache.get(Item_ID)
                    if (
                        row in bill_data.values()
                    ):  # Checking if row is already in use [Checking for over-writing] [Deleting from bill_data]
                        KEY_PRESENT = True  # If duplicate?
                        if bill_data.get(Item_ID, None) is None:
                            KEY_PRESENT = False
                        if not KEY_PRESENT:  #
                            self.setBillColumn(row, BillTableColumn.Qnty, 1)
                            self.setBillColumn(row, BillTableColumn.Disc_prcnt, 0)
                            self.setBillColumn(row, BillTableColumn.Disc, 0)
                            self.setBillColumn(row, BillTableColumn.Price, 0)
                            for key in bill_data.keys():
                                if bill_data[key] == row:
                                    break
                            bill_data.pop(key, None)
                            self.setCellTracking(True)
                            self.handle_cell_change(row, col)
                            return

                    if data is not None:
                        if Item_ID in bill_data.keys():  # Deals with duplicate entries
                            try:
                                self.setCellTracking(False)
                            except:
                                pass
                            if row != bill_data[Item_ID]:
                                self.setBillColumn(row, BillTableColumn.Id)
                                self.setBillColumn(row, 0)
                            row = bill_data[Item_ID]
                            qnty = int(self.getText(row, BillTableColumn.Qnty))
                            self.setBillColumn(row, BillTableColumn.Qnty, str(qnty + 1))
                            try:
                                Quantity = int(self.getText(row, BillTableColumn.Qnty))
                                Rate = int(self.getText(row, BillTableColumn.Rate))
                                Disc_Prc = float(self.getText(row, BillTableColumn.Disc_prcnt))
                                Price = Quantity * Rate
                                disc_amt = Price * Disc_Prc / 100
                                self.setBillColumn(
                                    row, BillTableColumn.Price, round(Price - disc_amt, 2)
                                )
                                self.setBillColumn(row, BillTableColumn.Disc, round(disc_amt, 2))
                            except Exception as e:
                                print(f"Error! {e}")

                            finally:
                                self.setCellTracking(True)
                        else:  # New Entry
                            Item_Name, Item_Rate = data["name"], data["sp"]
                            self.setBillColumn(
                                row, BillTableColumn.Name, Item_Name
                            )  # Set item in table
                            self.setBillColumn(row, BillTableColumn.Rate, Item_Rate)
                            self.setBillColumn(row, 0, row + 1)
                            self.setBillColumn(row, BillTableColumn.Disc_prcnt, 0)
                            self.setBillColumn(row, BillTableColumn.Disc, 0)
                            self.setBillColumn(row, BillTableColumn.Qnty, 1)
                            self.setBillColumn(row, BillTableColumn.Price, Item_Rate)
                            bill_data[Item_ID] = row
                            press("down")
                    else:  # If data from db is NONE  => New data (Custom)
                        if (
                            Item_ID in bill_data.keys()
                        ):  # Checking for duplicate entry(if duplicate...)
                            self.setBillColumn(row, BillTableColumn.Id)
                            row = bill_data[Item_ID]
                            qnty = int(self.getText(row, BillTableColumn.Qnty))
                            self.setBillColumn(row, BillTableColumn.Qnty, qnty + 1)
                            try:
                                Rate = int(self.getText(row, BillTableColumn.Rate))
                                dis = float(self.getText(row, BillTableColumn.Disc_prcnt))
                                p = (qnty + 1) * Rate
                                Price = p * (1 - (dis / 100))
                                self.setBillColumn(row, BillTableColumn.Disc, p - Price)
                                self.setBillColumn(row, BillTableColumn.Price, Price)
                            except:
                                pass
                            pass
                        else:  # If a new non-recurring entry not in db
                            self.setBillColumn(row, 0, row + 1)
                            self.setBillColumn(row, BillTableColumn.Disc, 0)
                            self.setBillColumn(row, BillTableColumn.Disc_prcnt, 0)
                            self.setBillColumn(row, BillTableColumn.Qnty, 1)
                            bill_data[Item_ID] = row
                            press("right")
                except:
                    pass
                self.setCellTracking(True)
            elif col == BillTableColumn.Qnty:  # Change in Quantity Column
                try:
                    self.setCellTracking(False)
                    Quantity = int(self.getText(row, BillTableColumn.Qnty))
                    Rate = int(self.getText(row, BillTableColumn.Rate))
                    Price = Quantity * Rate
                    try:
                        Discount_prct = float(self.getText(row, BillTableColumn.Disc_prcnt))
                        Discount = Price * (Discount_prct / 100)
                        Net_Price = Price - Discount
                        self.setBillColumn(row, BillTableColumn.Price, Net_Price)
                        self.setBillColumn(row, BillTableColumn.Disc, round(Discount, 2))
                    except:
                        Discount = int(self.getText(row, BillTableColumn.Disc))
                        Net_Price = Price - Discount
                        self.setBillColumn(row, BillTableColumn.Price, Net_Price)
                        Discount_prct = Discount * 100 / Net_Price
                        self.setBillColumn(
                            row, BillTableColumn.Disc_prcnt, round(Discount_prct, 2)
                        )  # Should be verifiedd
                    press(["down"] + ["left"] * 3)
                    self.setCellTracking(True)
                except:
                    pass
            elif col == BillTableColumn.Disc_prcnt:  # Change in Discount Percent
                try:
                    self.setCellTracking(False)
                    try:
                        Discount_Percentage = float(self.getText(row, BillTableColumn.Disc_prcnt))
                    except ValueError:
                        Discount_Percentage = 0
                        self.setBillColumn(row,col, 0)
                    Quantity = int(self.getText(row, BillTableColumn.Qnty))
                    Rate = int(self.getText(row, BillTableColumn.Rate))
                    Price = Quantity * Rate
                    Discount = Price * (Discount_Percentage / 100)
                    Price_disc = Price - Discount
                    self.setBillColumn(row, BillTableColumn.Price, Price_disc)
                    self.setBillColumn(row, BillTableColumn.Disc, round(Discount, 2))
                    self.setCellTracking(True)
                except:
                    pass
            elif col == BillTableColumn.Disc:  # Change in Discount price
                try:
                    self.setCellTracking(False)
                    try:
                        Discount = int(self.getText(row, BillTableColumn.Disc))
                    except ValueError:
                        Discount = 0
                        self.setBillColumn(row,col, 0)
                    Quantity = int(self.getText(row, BillTableColumn.Qnty))
                    Rate = int(self.getText(row, BillTableColumn.Rate))
                    Price = Quantity * Rate
                    Price_disc = Price - Discount
                    self.setBillColumn(row, BillTableColumn.Price, Price_disc)
                    Disc_perc = (Discount / Price) * 100
                    self.setBillColumn(row, BillTableColumn.Disc_prcnt, round(Disc_perc, 2))
                    self.setCellTracking(True)
                except:
                    pass
            elif col == BillTableColumn.Rate:  # Change in rate column
                try:
                    self.setCellTracking(False)
                    Rate = int(self.getText(row, BillTableColumn.Rate))
                    Quantity = int(self.getText(row, BillTableColumn.Qnty))
                    Price = Quantity * Rate
                    Discount = int(self.getText(row, BillTableColumn.Disc_prcnt))
                    Disc_Price = Price * Discount / 100
                    self.setBillColumn(row, BillTableColumn.Rate, Rate)
                    self.setBillColumn(row, BillTableColumn.Disc, round(Disc_Price, 2))
                    self.setBillColumn(row, BillTableColumn.Price, round((Price - Disc_Price), 2))
                    self.setCellTracking(True)
                except:
                    try:
                        self.setCellTracking(True)
                        pass
                    except:
                        pass
            elif col == BillTableColumn.Name:  # Change in Name column
                try:
                    self.setCellTracking(False)
                    name = self.getText(row, BillTableColumn.Name)
                    self.setBillColumn(row, BillTableColumn.Name, name)
                    self.setBillColumn(row, 0, row + 1)
                    if self.getText(row, BillTableColumn.Price) in [None, ""]:
                        self.setBillColumn(row, BillTableColumn.Price, 0)
                        self.setBillColumn(row, BillTableColumn.Disc, 0)
                        self.setBillColumn(row, BillTableColumn.Disc_prcnt, 0)
                    if self.getText(row, BillTableColumn.Qnty) in [None, ""]:
                        self.setBillColumn(row, BillTableColumn.Qnty, 1)
                except:
                    pass
                try:
                    self.setCellTracking(True)
                except:
                    pass

            try:  # Net Totals and discounts calculation
                self.CalcTotal()
                self.setCellTracking(True)
            except:
                try:
                    self.setCellTracking(True)
                    pass
                except:
                    pass

    def CalcTotal(self):
        global total
        net_total = int()
        total = float()
        discount = float()
        dsc_list: list[int | float] = []
        qnty_list: list[int] = []
        try:
            try:
                self.setCellTracking(False)
            except:
                pass
            for key in bill_data.keys():
                try:
                    total += float((self.getText(bill_data[key], BillTableColumn.Price)))
                except:
                    pass
                try:
                    disc = float(self.getText(bill_data[key], BillTableColumn.Disc))
                    discount += disc
                    dsc_list.append(disc)
                except:
                    pass
                try:
                    qnty = int(self.getText(bill_data[key], BillTableColumn.Qnty))
                    qnty_list.append(qnty)
                except:
                    pass

        except:
            pass
        self.Net_Discount_Label.setText(  
            "Net Discount    : " + str(round(discount, 2))
        )
        net_total = round(total + discount, 2)  
        self.Total_Label.setText(  
            "Total                 : " + str(round(total, 2))
        )
        self.Net_Total_Label.setText(  
            "Net Total          : " + str(net_total)
        )
        self.Bill_Time_Label.setText(  
            "Bill Time : {}".format(datetime.now().time().strftime("%H:%M:%S"))
        )
        return {
            "total": total,
            "net_Total": total + discount,
            "discount": discount,
            "dsc_list": dsc_list,
            "qnty_list": qnty_list,
        }

    def log_bill(self):
        try:
            if len(bill_data) == 0:
                return
        except:
            return

        final = self.CalcTotal()
        discount = float(final.get("discount", 0))
        nettotal = float(final.get("net_Total", 0))
        global Bill_No

        # Define the content of your bill
        company_name = "Fashion Paradise"
        address1 = "No. 1, Richwood Avenue, Market Road,"
        address2 = "Thaiyur - 603 103."
        bill_number = Bill_No
        bill_date = date.today().strftime("%d.%m.%Y")
        bill_time = datetime.now().time().strftime("%H:%M:%S")
        billed_by = "{} ({})".format(*User.getNameDesignation())

        # Set the font and font size
        font_name = "Helvetica"
        font_size = 10
        line_height = font_size * 1.2

        # Calculate the height of the content
        # content_height = 1.7 * inch + line_height * len(bill_data) + 0.8 * inch#-.05
        content_height = 11.9 * inch
        # Create a new canvas with a page size of 3 inches wide and dynamic height
        pdf_path = f"Bills/{Bill_No}.pdf"
        c = canvas.Canvas(pdf_path, pagesize=(5 * inch, content_height))
        c.setPageSize((3 * inch, 11.7 * inch))
        # Set the font and font size
        c.setFont("Helvetica-Bold", 16)
        # Add text to the canvas
        c.drawString(0.5 * inch, content_height - 0.4 * inch, company_name)

        c.setFont(font_name, font_size - 2)
        c.drawString(0.48 * inch, content_height - 0.6 * inch, address1)
        c.drawString(0.93 * inch, content_height - 0.75 * inch, address2)

        c.setFont(font_name, font_size - 1)
        c.drawString(0.1 * inch, content_height - 1 * inch, f"Bill No: {bill_number}")
        c.drawString(1.8 * inch, content_height - 1.2 * inch, f"Bill Date: {bill_date}")
        c.drawString(0.1 * inch, content_height - 1.2 * inch, f"Bill Time: {bill_time}")
        c.drawString(1.8 * inch, content_height - 1 * inch, f"Billed By: {billed_by.split()[0]}")

        c.setFont(font_name + "-Bold", font_size - 1)
        # Add table headers
        c.drawString(0.06 * inch, content_height - 1.5 * inch, "S.No.")
        c.drawString(0.74 * inch, content_height - 1.5 * inch, "Name")
        c.drawString(1.74 * inch, content_height - 1.5 * inch, "Rate")
        c.drawString(2.1 * inch, content_height - 1.5 * inch, "Qnty")
        c.drawString(2.46 * inch, content_height - 1.5 * inch, "Amount")

        # Add table data
        y = content_height - 1.72 * inch
        c.setFont(font_name, font_size - 2)
        sno = 1
        for key in bill_data.keys():
            name = self.getText(bill_data[key], BillTableColumn.Name)
            if name != "":
                quantity = self.getText(bill_data[key], BillTableColumn.Qnty)
                rate = self.getText(bill_data[key], BillTableColumn.Rate)
                amount = round(int(quantity) * int(rate), 2)
                c.drawString(0.17 * inch, y, str(sno))
                c.drawString(0.48 * inch, y, name[:22])
                c.drawString(1.77 * inch, y, rate)
                c.drawString(2.18 * inch, y, quantity)
                c.drawString(2.57 * inch, y, str(amount))
                self.resetRow(bill_data[key])
                y -= line_height
                sno += 1
            else:
                self.resetRow(bill_data[key])
        # Add total and net total
        c.setFont('Helvetica', font_size + 1)
        c.drawString(1 * inch, y - 0.15 * inch, f"Total        : Rs. {str(round(nettotal, 2))}")
        c.drawString(1 * inch, y - 0.35 * inch, f"Discount  : Rs. {str(discount)}")
        c.setFont('Helvetica-Bold', font_size + 1)
        c.drawString(1 * inch, y - 0.55 * inch, f"Net Total : Rs. {str(round(nettotal-discount, 2))}/-")   

        # Save the canvas to generate the PDF file
        c.save()
        location = path.abspath(f"{DIREC}/Bills/{Bill_No}.pdf")
        ShellExecute(0, "print", location, None, ".", 0)  # type: ignore
        items_qry_data = {
            "bill_no": Bill_No,
            "date": date.today().strftime("%d.%m.%Y")
            + ", "
            + datetime.now().time().strftime("%H:%M:%S"),
            "items": list(bill_data.keys()),
            "discounts": final["dsc_list"],
            "quantity": final["qnty_list"],
            "total": round(nettotal - discount, 2),
        }
        print(items_qry_data)
        json_data = dumps(items_qry_data)
        post(f"{url}//bills", json=json_data)
        bill_data.clear()
        self.CalcTotal()
        self.setup(init=True)

    def logout(self):
        confirmation_dialog = QMessageBox(self)
        confirmation_dialog.setWindowTitle("Confirmation")
        confirmation_dialog.setText("Are you sure you want to logout?")
        confirmation_dialog.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        confirmation_dialog.setIcon(QMessageBox.Icon.Question)
        reply = confirmation_dialog.exec()
        if reply == QMessageBox.StandardButton.Yes:
            User.toggleLoggingOut()
            self.menuSales.setEnabled(False)  
            self.menuStock.setEnabled(False)  
            self.New_Bill_Tab.setEnabled(False)  
            information_dialog = QMessageBox()
            information_dialog.setWindowTitle("Success!")
            information_dialog.setText("Logged out successfully!")
            information_dialog.setIcon(
                QMessageBox.Icon.Information
            )  # Optional: Information icon
            information_dialog.setStandardButtons(
                QMessageBox.StandardButton.Ok
            )  # Only OK button
            app.closeAllWindows()
            information_dialog.exec()
            information_dialog.close()
            self.close()
            exit(True)
        else:
            return


if __name__ == "__main__":
    Init()
