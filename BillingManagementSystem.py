# Imports
import string
from tkinter.filedialog import askopenfilename
from typing import Generator
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
from urllib.request import Request, urlopen
from json import loads
from datetime import datetime, date
from os import getenv as cred_
from sys import exit as exi
from atexit import register as exit_manager

# Global Declaration of Column Position
Name_Col, Rate_Col, ID_Col, Qnty_Col, Disc_prcnt_Col, Disc_Col, Price_Col = 2,3,1,4,5,6,7
punc = string.punctuation
# Global Variables
Admin = False  # Used for Authentication and permissions
Name = str()  # Name of the User
logging_out = False
Designation = None
User = str()  # Stores the current user info
bill_data = dict()  # Stores data as {Item_ID : Row} Acts as temp for Current Bill items
Bill_No = int()

def get_Api() -> str:
    """Returns the API URL for the server"""
    from pickle import load
    with open("Resources\\sak.dat", 'rb') as file:
        return load(file).decode("utf-32")
    
url = get_Api()

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
    global Admin
    Admin = False
    Login()

def main():
    global app
    app = QApplication([])
    window = BMS_Home_GUI()
    exi(app.exec())

def Bill_Number() -> Generator:
    global cur
    #cur.execute("SELECT * FROM bills ORDER BY bill_no DESC LIMIT 1")
    Latest_Bill = None
    if Latest_Bill is None:
        Latest_Bill_No = 10000
    else:
        Latest_Bill_No = Latest_Bill[0]
    for Bill_Number in range(Latest_Bill_No + 1, 100000):
        yield Bill_Number
    
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
        command=lambda: ValidateEntry(),
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
    def ValidateEntry():
        if ValidateEntry_():
            Auth(username_entry.get(),password_entry.get())
    def ValidInp(val,usr: bool = False):
        if usr:
            return username_entry.get().isalpha()
        else:
            pw :str= password_entry.get()
            intersect = set(pw).intersection(punc)
            if len(intersect)==0 or (len(intersect) == 1 and {'_'} == intersect):
                return True
            return False
    
    def ValidateEntry_() -> None | bool:
        if ValidInp(username_entry.get(),usr=True) and ValidInp(password_entry.get()):
            return True
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
        else:
            messagebox.showerror(
                title="Authentication Error!",
                message="Username or Password must contain only letters and numbers!"
            )
    #Final
    frame.pack()
    login_window.mainloop()
#Authentication
def Auth(user :str, pwd :str) -> None:
    URL = f"{url}//authenticate//{user}//{pwd}"
    print(URL)
    req = Request(URL)
    response_ =  urlopen(req)
    response = response_.read().decode()
    result = loads(response)
    print(result,response)
    #Comparing Hashed Passwords
    if result is not None:  
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
        main()  

    else:
        messagebox.showerror(
            title="Authentication Error!", message="Wrong Username or Password"
        )

Bill_No_Gen: Generator = Bill_Number()  # Memory Efficient way to generate bill no. successively (Generator Object)


class BMS_Home_GUI(QMainWindow):
    def __init__(self):
        """
        Should Set the Column width from code appropriately
        """
        global Bill_No
        Bill_No = next(Bill_No_Gen)
        super(BMS_Home_GUI, self).__init__()
        uic.loadUi("BMS_Home_GUI.ui", self)  # type:ignore
        aspect_ratio = 16 / 9  # aspect ratio
        min_height = 900
        min_width = int(min_height * aspect_ratio)
        self.setMinimumSize(min_width, min_height)
        self.setWindowTitle("BMS -botpeter17")
        icon = QIcon("My_Icon.ico")
        self.setWindowIcon(icon)
        if Admin:
            self.menuSales.setEnabled(True)  # type:ignore
            self.menuStock.setEnabled(True)  # type:ignore
            self.New_Bill_Tab.setEnabled(True)  # Should Set back to Flase at exit # type:ignore
        self.show()
        self.setup()

    def setup(self):
        global Bill_No
        self.setTheme("Qt resources//Theme//Default.qss")
        self.Bill_Number_Label.setText("Bill No    : {}".format((Bill_No)))  # type:ignore
        self.Bill_Date_Label.setText("Bill Date : {}".format(date.today().strftime("%B %d, %Y")))  # type:ignore
        self.Billed_By_Label.setText("Billed By : {} ({})".format(Name, Designation))  # type:ignore
        self.Bill_Time_Label.setText("Bill Time :{}".format(datetime.now().time().strftime("%H:%M:%S")))# type:ignore
        self.actionLogout.triggered.connect(lambda: self.logout())  # type:ignore
        self.actionThemes.triggered.connect(lambda: self.setTheme())  # type:ignore
        self.Profile.triggered.connect(lambda: Profile_(User)) # Should Change after defining Profile GUI  
        self.Bill_Table.setColumnCount(8)  # type:ignore
        self.Bill_Table.setRowCount(26)  # type:ignore
        self.Bill_Table.cellChanged.connect(self.handle_cell_change)  # type:ignore
        self.Print_Button.clicked.connect(self.log_bill)  # type:ignore
        # Setting Column Widths
        # Didn't define the width of price col to allow resizing
        self.Bill_Table.setColumnWidth(0, 100)  # type:ignore
        self.Bill_Table.setColumnWidth(ID_Col, 150)  # type:ignore
        self.Bill_Table.setColumnWidth(Name_Col, 350)  # type:ignore
        self.Bill_Table.setColumnWidth(Rate_Col, 150)  # type:ignore
        self.Bill_Table.setColumnWidth(Qnty_Col, 150)  # type:ignore
        self.Bill_Table.setColumnWidth(Disc_prcnt_Col, 175)  # type:ignore
        self.Bill_Table.setColumnWidth(Disc_Col, 175)  # type:ignore

    def closeEvent(self, event):
        global logging_out
        if logging_out:
            return
        reply = QMessageBox.question(
            self,
            "Exit?",
            "Are you sure you want to quit?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            global Admin
            Admin = False
            event.accept()
        else:
            event.ignore()
        """
        @atexit.register
def closure():
    try:
        if not(cur.closed):
            con.close()
    except:
        pass
    global Admin
    Admin=False"""

    def setTheme(self, path: None | str = None) -> None:
        try:
            if path is None:
                path = askopenfilename(
                    title="Select Theme",
                    initialdir="Qt Resources//Themes//",
                    filetypes=(("QSS", "*.qss"),),
                )
        except:
            pass
        try:
            with open(path) as f:  # type:ignore
                stylesheet = f.read()
                self.setStyleSheet(stylesheet)
                self.setup()
        except:
            pass

    def setBillColumn(self, row: int, column: int, value: str | int | float = ""):
        temp = QTableWidgetItem(str(value))
        temp.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.Bill_Table.setItem(row, column, temp)  # type:ignore

    def setCellTracking(self, mode: bool) -> None:
        if not mode:
            self.Bill_Table.cellChanged.disconnect(self.handle_cell_change)  # type:ignore
            return
        self.Bill_Table.cellChanged.connect(self.handle_cell_change)  # type:ignore

    def getText(self, row: int, column: int) -> str:
        return self.Bill_Table.item(row, column).text()  # type:ignore

    def resetRow(self, row: int) -> None:
        for col in range(8):
            self.setBillColumn(row, col, "")

    def handle_cell_change(self, row, col):
        if row is not None:
            if col == ID_Col:  # Change in ID Column
                self.setCellTracking(False)
                try:
                    s = self.getText(row, ID_Col)
                    Item_ID = int(s)
                    del s
                    if Item_ID not in bill_data:
                        self.setBillColumn(row, ID_Col, Item_ID)
                except:  # Convertion Error (str -> int)
                    if (
                        self.Bill_Table.item(row, ID_Col).text() == ""  # type:ignore
                        or self.Bill_Table.item(row, ID_Col).text()== None  # type:ignore
                    ):
                        self.resetRow(row)
                try:
                    req = Request(f"{url}//items//{Item_ID}")
                    response = urlopen(req)
                    data = response.read().decode("utf-8")
                    data = loads(data)
                    if (row in bill_data.values()):  # Checking if row is already in use [Checking for over-writing] [Deleting from bill_data]
                        """item=QTableWidgetItem('')
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.Bill_Table.setItem(row,Name_Col,item)
                        item=QTableWidgetItem('')
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.Bill_Table.setItem(row,Rate_Col,item)"""
                        item_id = self.getText(row, ID_Col)
                        """if bill_data[item_id]==row:
                            self.setBillColumn(row,Qnty_Col, int(self.getText(row,Qnty_Col))+1)
                            discount = self.getText(row,Disc_prcnt_Col)
                            """
                        if bill_data[item_id] != row:
                            self.setBillColumn(row, Qnty_Col, 1)
                            self.setBillColumn(row, Disc_prcnt_Col, 0)
                            self.setBillColumn(row, Disc_Col, 0)
                            self.setBillColumn(row, Price_Col, 0)
                            for key in bill_data.keys():
                                if bill_data[key] == row:
                                    break
                            bill_data.pop(key, None)

                    if data is not None:
                        if Item_ID in bill_data.keys():  # Deals with duplicate entries
                            self.setBillColumn(row, ID_Col)
                            row = bill_data[Item_ID]
                            qnty = int(self.getText(row, Qnty_Col))
                            self.setBillColumn(row, Qnty_Col, str(qnty + 1))
                            try:
                                Quantity = int(self.getText(row, Qnty_Col))
                                Rate = int(self.getText(row, Rate_Col))
                                Price = Quantity * Rate
                                self.setBillColumn(row, Price_Col, Price)
                            except Exception as e:
                                print(f"Error! {e}")
                            pass
                        else:  # New Entry
                            Item_Name, Item_Rate = data['name'],data['sp']
                            self.setBillColumn(row, Name_Col, Item_Name)  # Set item in table
                            self.setBillColumn(row, Rate_Col, Item_Rate)
                            self.setBillColumn(row, 0, row + 1)
                            self.setBillColumn(row, Disc_prcnt_Col, 0)
                            self.setBillColumn(row, Disc_Col, 0)
                            self.setBillColumn(row, Qnty_Col, 1)
                            self.setBillColumn(row, Price_Col, Item_Rate)
                            bill_data[Item_ID] = row
                    else:  # If data from db is NONE  => New data (Custom)
                        if (Item_ID in bill_data.keys()):  # Checking for duplicate entry(if duplicate...)
                            self.setBillColumn(row, ID_Col)
                            row = bill_data[Item_ID]
                            qnty = int(self.getText(row, Qnty_Col))
                            self.setBillColumn(row, Qnty_Col, qnty + 1)
                            try:
                                Quantity = int(self.getText(row, Qnty_Col))
                                Rate = int(self.getText(row, Rate_Col))
                                dis = float(self.getText(row, Disc_prcnt_Col))
                                p = Quantity * Rate
                                Price = p * (1 - (dis / 100))
                                self.setBillColumn(row, Disc_Col, p - Price)
                                self.setBillColumn(row, Price_Col, Price)
                            except:
                                pass
                            pass
                        else:  # If a new non-recurring entry not in db
                            self.setBillColumn(row, 0, row + 1)
                            self.setBillColumn(row, Disc_Col, 0)
                            self.setBillColumn(row, Disc_prcnt_Col, 0)
                            self.setBillColumn(row, Qnty_Col, 1)
                            bill_data[Item_ID] = row
                except:
                    pass
                self.setCellTracking(True)
            elif col == Qnty_Col:  # Change in Quantity Column
                try:
                    self.setCellTracking(False)
                    Quantity = int(self.getText(row, Qnty_Col))
                    Rate = int(self.getText(row, Rate_Col))
                    Price = Quantity * Rate
                    try:
                        Discount_prct = float(self.getText(row, Disc_prcnt_Col))
                        Discount = Price * (Discount_prct / 100)
                        Net_Price = Price - Discount
                        self.setBillColumn(row, Price_Col, Net_Price)
                        self.setBillColumn(row, Disc_Col, round(Discount, 2))
                    except:
                        Discount = int(self.getText(row, Disc_Col))
                        Net_Price = Price - Discount
                        self.setBillColumn(row, Price_Col, Net_Price)
                        Discount_prct = Discount * 100 / Net_Price
                        self.setBillColumn(row, Disc_prcnt_Col, round(Discount_prct, 2))  # Should be verifiedd
                    self.setCellTracking(True)
                except:
                    pass
            elif col == Disc_prcnt_Col:  # Change in Discount Percent
                try:
                    self.setCellTracking(False)
                    Discount_Percentage = int(self.getText(row, Disc_prcnt_Col))
                    Quantity = int(self.getText(row, Qnty_Col))
                    Rate = int(self.getText(row, Rate_Col))
                    Price = Quantity * Rate
                    Discount = Price * (Discount_Percentage / 100)
                    Price_disc = Price - Discount
                    self.setBillColumn(row, Price_Col, Price_disc)
                    self.setBillColumn(row, Disc_Col, round(Discount, 2))
                    self.setCellTracking(True)
                except:
                    pass
            elif col == Disc_Col:  # Change in Discount price
                try:
                    self.setCellTracking(False)
                    Discount = int(self.getText(row, Disc_Col))
                    Quantity = int(self.getText(row, Qnty_Col))
                    Rate = int(self.getText(row, Rate_Col))
                    Price = Quantity * Rate
                    Price_disc = Price - Discount
                    self.setBillColumn(row, Price_Col, Price_disc)
                    Disc_perc = (Discount / Price) * 100
                    self.setBillColumn(row, Disc_prcnt_Col, round(Disc_perc, 2))
                    self.setCellTracking(True)
                except:
                    pass
            elif col == Rate_Col:  # Change in rate column
                try:
                    self.setCellTracking(False)
                    Rate = int(self.getText(row, Rate_Col))
                    Quantity = int(self.getText(row, Qnty_Col))
                    Price = Quantity * Rate
                    Discount = int(self.getText(row, Disc_prcnt_Col))
                    Disc_Price = Price * Discount / 100
                    self.setBillColumn(row,Rate_Col,Rate)
                    self.setBillColumn(row, Disc_Col, round(Disc_Price, 2))
                    self.setBillColumn(row, Price_Col, round((Price - Disc_Price), 2))
                    self.setCellTracking(True)
                except:
                    try:
                        self.setCellTracking(True)
                        pass
                    except:
                        pass
            elif col == Name_Col:   #Change in Name column
                try:
                    self.setCellTracking(False)
                    name = self.getText(row,Name_Col)
                    self.setBillColumn(row,Name_Col,name)
                    self.setBillColumn(row,0,row+1)
                    if self.getText(row,Price_Col) in [None, ""]:
                        self.setBillColumn(row, Price_Col, 0)
                        self.setBillColumn(row, Disc_Col, 0)
                        self.setBillColumn(row, Disc_prcnt_Col, 0)
                    if self.getText(row,Qnty_Col) in [None, ""]:
                        self.setBillColumn(row,Qnty_Col,1)
                except:
                    pass
                try:
                    self.setCellTracking(True)
                except:
                    pass

            global total
            net_total = int()
            total = float()
            discount = float()
            try:  # Net Totals and discounts calculation
                for key in bill_data.keys():
                    self.setCellTracking(False)
                    try:
                        total += float((self.getText(bill_data[key], Price_Col)))
                    except:
                        pass
                    try:
                        discount += float(self.getText(bill_data[key], Disc_Col))
                    except:
                        pass
                    self.Net_Discount_Label.setText("Net Discount    : " + str(round(discount, 2)))     # type:ignore
                    net_total = round(total + discount, 2)  # type:ignore
                    self.Total_Label.setText("Total                  : " + str(round(total, 2)))  # type:ignore
                    self.Net_Total_Label.setText("Net Total          : " + str(net_total))  # type:ignore
                    self.Bill_Time_Label.setText("Bill Time :{}".format(datetime.now().time().strftime("%H:%M:%S")))  # type:ignore
                    self.setCellTracking(True)
            except:
                try:
                    self.setCellTracking(True)
                    pass
                except:
                    pass

    def log_bill(self):
        try:
            if total == 0:
                return
        except:
            return
        global Bill_No, cur
        with open("Bills//{}.txt".format((Bill_No)), "w") as Bill:
            Bill.writelines("")
            """
            Should add bill(text) content after determining the Paper size
            """
        ...
        cur.execute(
            "insert into bills values ({},'{}',{},'{}')".format(
                Bill_No, (date.today().strftime("%d %B, %Y")), total, User
            )
        )
        con.commit()
        global bill_data
        for key in bill_data.keys():
            self.setBillColumn(bill_data[key], ID_Col, "")
        Bill_No = next(Bill_No_Gen)
        bill_data = (dict())  # reinitializing the item data stored and hence resetting the Table
        self.setup()

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
            global Admin, logging_out
            logging_out = True
            Admin = False
            self.menuSales.setEnabled(False)  # type:ignore
            self.menuStock.setEnabled(False)  # type:ignore
            self.New_Bill_Tab.setEnabled(False)  # type:ignore
            information_dialog = QMessageBox()
            information_dialog.setWindowTitle("Success!")
            information_dialog.setText("Logged out successfully!")
            information_dialog.setIcon(QMessageBox.Icon.Information)  # Optional: Information icon
            information_dialog.setStandardButtons(QMessageBox.StandardButton.Ok)  # Only OK button
            app.closeAllWindows()
            information_dialog.exec()
            information_dialog.close()
            self.close()
            exit(True)
        else:
            return

if __name__ == '__main__':
    Init()