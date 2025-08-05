# Imports
import string
import platform
import subprocess
import os
from os import path, makedirs
from enum import StrEnum, auto
from typing import LiteralString
from requests import post
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from pathlib import Path
from pyautogui import press
from tkinter.filedialog import askopenfilename
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
from PyQt6.QtCore import QThread, Qt, pyqtSignal
from urllib.request import Request, urlopen
from json import dumps, loads
from datetime import datetime, date
from sys import exit as exi
import logging
# Custom Imports
from utils.server import get_Api, run_check_server_periodically
from utils.types import User, Bill_ as Bill
from utils.enums import *
from utils.printer import ReceiptPrinter
pathJoiner = path.join
abspath = path.abspath

#Platform dependant
CURR_PLATFORM = platform.system()
if CURR_PLATFORM == 'Windows':
    from win32api import ShellExecute
elif CURR_PLATFORM == 'Linux':
    import subprocess

printer = ReceiptPrinter(0x154F, 0x154F, interface=1)
DIREC = Path(__file__).resolve().parent

#Importing Punctuations for Password Validation
punc : LiteralString = string.punctuation

url: str = get_Api()

# Configure logging
logging.basicConfig(
    filename="bms.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logging.info("Billing Management System started.")


def Init() -> None:
    logging.info("Init: Attempting to connect to server...")
    try:
        if_connected_req = Request(f"{url}//connected")
        with urlopen(if_connected_req) as responsee:
            if loads(responsee.read().decode("utf-8")):
                logging.info("Init: Connected to server successfully.")
                messagebox.showinfo("Success!", "Connected to the server successfully")
            else:
                logging.error("Init: Failed to connect to the server.")
                messagebox.showerror("Error!", "Failed to connect to the server")
    except Exception as e:
        logging.error(f"Init: Exception during connection: {e}", exc_info=True)
        messagebox.showerror("Error", f"Error: {e}")
        exit(True)
    run_check_server_periodically()
    makedirs(pathJoiner(DIREC, "Bills"), exist_ok=True)
    Login()


def main():
    global app
    logging.info("Initializing QApplication and main window.")
    if CURR_PLATFORM == 'Linux':
        logging.info("Linux environment detected, setting Qt platform settings")
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseDesktopOpenGL)
        os.environ['QT_QPA_PLATFORM'] = 'xcb'
    app = QApplication([])
    window = BMS_Home_GUI()
    window.showMaximized()
    logging.info("Main window shown. Application event loop starting.")
    try:
        app.exec()     #    exi(app.exec()) => Original
        logging.info("Application exited normally.")
    except Exception as e:
        logging.error(f"Application crashed: {e}", exc_info=True)
        raise

def Login() -> None:
    global login_window
    logging.info("Login window opened.")
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
        command=lambda: ValidateEntry(username_entry.get(), password_entry.get()),
        bg="#ffffff",
        fg="#FF3399",
    )
    login_window.bind("<Return>", lambda event: ValidateEntry(username_entry.get(), password_entry.get()))
    # Layout
    login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
    username_label.grid(row=1, column=0)
    username_entry.grid(row=1, column=1, pady=20)
    password_label.grid(row=2, column=0)
    password_entry.grid(row=2, column=1, pady=20)
    login_button.grid(row=3, column=0, columnspan=2, pady=30)

    # Checking_Input
    def ValidateEntry(username, password):
        logging.info(f"Login attempt: username='{username}'")
        if len(username) == 0:
            logging.warning("Login failed: Username is empty.")
            messagebox.showerror(
                title="Authentication Error!", message="Enter the Username!"
            )
        elif len(password) == 0:
            logging.warning(f"Login failed: Password is empty for username='{username}'")
            messagebox.showerror(
                title="Authentication Error!", message="Enter the Password!"
            )
        elif not username.isalnum():
            logging.warning(f"Login failed: Invalid characters in username or password for username='{username}'")
            messagebox.showerror(
                title="Authentication Error!",
                message="Username or Password must contain only letters and numbers!",
            )
        else:
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
    logging.info("Login window closed.")


# Authentication
def Auth(user: str, pwd: str) -> None:
    logging.info(f"Auth: Authentication attempt for username='{user}'")
    URL = f"{url}//authenticate//{user}//{pwd}"
    try:
        req = Request(URL)
        response_ = urlopen(req)
        response = response_.read().decode()
        result = loads(response)
        # Comparing Hashed Passwords
        if result is not None:
            User.update(uid=user, **result)
            logging.info(f"Auth: Authentication successful for username='{user}' (admin={User.isAdmin()})")
            Bill.Init()
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
            logging.warning(f"Auth: Authentication failed for username='{user}' (wrong credentials)")
            messagebox.showerror(
                title="Authentication Error!", message="Wrong Username or Password"
            )
    except Exception as e:
        logging.error(f"Auth: Exception during authentication for username='{user}': {e}", exc_info=True)
        messagebox.showerror(
            title="Authentication Error!", message=f"Authentication failed due to error: {e}"
        )

class WorkerThread(QThread):
    updateStock = pyqtSignal()
    viewStock = pyqtSignal()

    def __init__(self, window_name):
        logging.info(f"WorkerThread.__init__: Initializing worker thread for window '{window_name}'.")
        super().__init__()
        self.window_name = window_name
        logging.info(f"WorkerThread.__init__: Exited.")

    def run(self):
        logging.info(f"WorkerThread.run: Running worker thread for window '{self.window_name}'.")
        try:
            if self.window_name == WindowName.UpdateStock:
                self.updateStock.emit()
                logging.info("WorkerThread.run: updateStock emitted.")
            elif self.window_name == WindowName.ViewStock:
                self.viewStock.emit()
                logging.info("WorkerThread.run: viewStock emitted.")
            else:
                logging.warning(f"WorkerThread.run: Unknown window name '{self.window_name}'.")
        except Exception as e:
            logging.error(f"WorkerThread.run: Exception occurred: {e}", exc_info=True)


class WindowName(StrEnum):
    UpdateStock = auto()
    ViewStock = auto()


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
    Update_Stock :QMenu
    View_Stock :QMenu

    def __init__(self):
        """
        Should Set the Column width from code appropriately
        """
        logging.info("BMS_Home_GUI: Initializing main window GUI.")
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
            logging.info("BMS_Home_GUI: User is admin, enabling admin menus.")
            self.menuSales.setEnabled(True)
            self.menuStock.setEnabled(True)
            self.New_Bill_Tab.setEnabled(True)  # Should Set back to Flase at exit
        self.show()
        self.setup()
        press("tab")
        logging.info("BMS_Home_GUI: Main window GUI initialized and shown.")

    def startThread(self, window_name):
        logging.info(f"BMS_Home_GUI: Starting worker thread for window '{window_name}'.")
        self.worker = WorkerThread(window_name)  #Thread Initialization
        # Connection signals to Different Windows
        self.worker.updateStock.connect(self.updateStock)
        self.worker.viewStock.connect(self.viewStock)
        #Starting the Thread
        self.worker.run()

    def updateStock(self):
        logging.info("BMS_Home_GUI.updateStock: Triggered.")
        try:
            from query_format_advanced import QueryFormatterGUI
            self.queryFormatter = QueryFormatterGUI()
            self.queryFormatter.showMaximized()
            logging.info("BMS_Home_GUI.updateStock: Stock window shown.")
        except Exception as e:
            logging.error(f"BMS_Home_GUI.updateStock: Error: {e}", exc_info=True)

    def viewStock(self):
        logging.info("BMS_Home_GUI: Opening view stock window.")
        from query_format_advanced import QueryFormatterGUI
        self.stockViewer = QueryFormatterGUI()
        self.stockViewer.loadStock(Bill.getItems())
        self.stockViewer.showMaximized()

    def setup(self, init: bool = False):
        logging.info(f"BMS_Home_GUI: Running setup (init={init}).")
        self.setTheme(pathJoiner("Resources", "Default.qss"))
        self.Bill_Number_Label.setText(  # type:ignore
            "Bill No    : {}".format(Bill.Get_Bill_No())
        )
        self.Bill_Date_Label.setText(  # type:ignore
            "Bill Date : {}".format(Bill.Get_Date())
        )
        self.Billed_By_Label.setText(
            "Billed By : {} ({})".format(*User.getNameDesignation())
        )
        self.Bill_Time_Label.setText(  # type:ignore
            "Bill Time : {}".format(Bill.Get_Time())
        )
        self.actionLogout.triggered.connect(lambda: self.logout())
        self.actionThemes.triggered.connect(lambda: self.setTheme())
        self.Update_Stock.triggered.connect(lambda: self.startThread(WindowName.UpdateStock))
        self.View_Stock.triggered.connect(lambda: self.startThread(WindowName.ViewStock))
        self.Profile.triggered.connect(
            lambda: Profile_(User)  # TODO:ignore
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
        logging.info("BMS_Home_GUI: Window close event triggered.")
        if User.isLoggingOut():
            logging.info("BMS_Home_GUI: User is logging out, allowing close.")
            return
        reply = QMessageBox.question(
            self,
            "Exit?",
            "Are you sure you want to quit?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            logging.info("BMS_Home_GUI: User confirmed exit, resetting user and closing window.")
            User.resetUser()
            event.accept()
        else:
            logging.info("BMS_Home_GUI: User cancelled exit, ignoring close event.")
            event.ignore()

    def setTheme(self, path: None | str = None) -> None:
        logging.info(f"BMS_Home_GUI.setTheme called with path={path}")
        try:
            if path is None:
                path = askopenfilename(
                    title="Select Theme",
                    initialdir=DIREC,
                    filetypes=(("QSS", "*.qss"),),
                )
                logging.info(f"Theme file selected: {path}")
        except Exception as e:
            logging.error(f"Error selecting theme file: {e}", exc_info=True)
        try:
            with open(path) as f:
                stylesheet = f.read()
                self.setStyleSheet(stylesheet)
                logging.info(f"Theme applied from file: {path}")
        except Exception as e:
            logging.error(f"Error applying theme from file '{path}': {e}", exc_info=True)

    def setBillColumn(self, row: int, column: int, value: str | int | float = ""):
        try:
            temp = QTableWidgetItem(str(value))
            temp.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.Bill_Table.setItem(row, column, temp)
        except Exception as e:
            logging.error(f"setBillColumn: Failed to set cell at row={row}, col={column} with value={value}: {e}", exc_info=True)

    def setCellTracking(self, mode: bool) -> None:
        try:
            if not mode:
                self.Bill_Table.cellChanged.disconnect(self.handle_cell_change)  # type:ignore
                logging.debug(f"setCellTracking: Disconnected cellChanged signal.")
                return
            self.Bill_Table.cellChanged.connect(self.handle_cell_change)  # type:ignore
            logging.debug(f"setCellTracking: Connected cellChanged signal.")
        except TypeError:
            logging.debug(f"setCellTracking: The Cell Tracking mode is already set to {mode}.")
        except Exception as e:
            logging.error(f"setCellTracking: Error setting mode={mode}: {e}", exc_info=True)

    def getText(self, row: int, column: int, dtype : type = str):
        try:
            data = self.Bill_Table.item(row, column)  # type:ignore
            if data:
                return dtype(data.text())
            return dtype()
        except Exception as e:
            logging.error(f"getText: Error getting text at row={row}, col={column}: {e}", exc_info=True)
            return dtype()

    def resetRow(self, row: int) -> None:
        try:
            for col in range(8):
                self.setBillColumn(row, col, "")
        except Exception as e:
            logging.error(f"resetRow: Error resetting row {row}: {e}", exc_info=True)

    def handle_cell_change(self, row, col):
        logging.info(f"BMS_Home_GUI.handle_cell_change called for row={row}, col={col}")
        if col == BillTableColumn.Id:  # Change in ID Column
            logging.debug(f"Cell change in ID column at row={row}")
            self.setCellTracking(False)
            try:
                Item_ID = self.getText(row, BillTableColumn.Id, int)
                logging.debug(f"Parsed Item_ID: {Item_ID}")
            except ValueError:  # Convertion Error (str -> int)
                logging.warning(f"ValueError parsing Item_ID at row={row}, col={col}")
                if (self.Bill_Table.item(row, BillTableColumn.Id).text() == ""):
                    self.resetRow(row)
                    Bill.remove_row_item(row)     #TODO: Implement
                    logging.info(f"Row {row} reset due to empty Item_ID")
                    return

            if Bill.contains(Item_ID):
                logging.info(f"Item_ID {Item_ID} already exists in Bill. Updating row {row}.")
                self.setCellTracking(False)
                self.setBillColumn(row, BillTableColumn.Id, Item_ID)

            try:
                data = Bill.Get_Item(Item_ID)
                logging.debug(f"Fetched data for Item_ID {Item_ID}: {data}")
                if Bill.isDuplicateRow(row):
                    KEY_PRESENT = True  # If duplicate?
                    if Bill.getCart().get(Item_ID) is None:
                        KEY_PRESENT = False
                    if not KEY_PRESENT:   #Row is duplicate.... Item in New
                        self.setBillColumn(row, BillTableColumn.Qnty, 1)
                        self.setBillColumn(row, BillTableColumn.Disc_prcnt, 0)
                        self.setBillColumn(row, BillTableColumn.Disc, 0)
                        self.setBillColumn(row, BillTableColumn.Price, 0)
                        '''for key in bill_data.keys():
                            if bill_data[key] == row:
                                break
                        bill_data.pop(key, None)'''
                        Bill.remove_row_item(row)
                        self.setCellTracking(True)
                        self.handle_cell_change(row, col)
                        return

                if data is not None:
                    if Bill.contains(Item_ID):  # Deals with duplicate entries
                        self.setCellTracking(False)
                        if row != Bill.getCart().get(Item_ID):
                            self.setBillColumn(row, BillTableColumn.Id)
                            self.setBillColumn(row, 0)
                        row = Bill.getRowNumber(Item_ID)
                        qnty = self.getText(row, BillTableColumn.Qnty, int)
                        self.setBillColumn(row, BillTableColumn.Qnty, str(qnty + 1))
                        try:
                            Quantity = self.getText(row, BillTableColumn.Qnty, int)
                            Rate = self.getText(row, BillTableColumn.Rate, float)
                            Disc_Prc = self.getText(row, BillTableColumn.Disc_prcnt, float)
                            Price = Quantity * Rate
                            disc_amt = Price * Disc_Prc / 100
                            self.setBillColumn(
                                row, BillTableColumn.Price, round(Price - disc_amt, 2)
                            )
                            self.setBillColumn(row, BillTableColumn.Disc, round(disc_amt, 2))
                        except Exception as e:
                            logging.error(f"Error updating duplicate row for Item_ID {Item_ID} at row {row}: {e}", exc_info=True)

                        finally:
                            self.setCellTracking(True)
                    else:  # New Entry
                        Item_Name, Item_Rate = data.get("name"), data.get("sp")
                        self.setBillColumn(
                            row, BillTableColumn.Name, Item_Name
                        )  # Set item in table
                        self.setBillColumn(row, BillTableColumn.Rate, Item_Rate)
                        self.setBillColumn(row, 0, row + 1)
                        self.setBillColumn(row, BillTableColumn.Disc_prcnt, 0)
                        self.setBillColumn(row, BillTableColumn.Disc, 0)
                        self.setBillColumn(row, BillTableColumn.Qnty, 1)
                        self.setBillColumn(row, BillTableColumn.Price, Item_Rate)
                        Bill.addItem(Item_ID, row)
                        press("down")
                else:  # If data from db is NONE  => New data (Custom)
                    logging.warning(f"No data found for Item_ID {Item_ID} at row {row}. Treating as custom entry.")
                    if Bill.contains(Item_ID):  # Checking for duplicate entry(if duplicate...)
                        self.setBillColumn(row, BillTableColumn.Id)
                        row = Bill.getRowNumber(Item_ID)
                        qnty = self.getText(row, BillTableColumn.Qnty, int)
                        self.setBillColumn(row, BillTableColumn.Qnty, qnty + 1)
                        try:
                            Rate = self.getText(row, BillTableColumn.Rate, float)
                            dis = self.getText(row, BillTableColumn.Disc_prcnt, float)
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
                        # bill_data[Item_ID] = row
                        Bill.addItem(Item_ID, row)
                        press("right")
            except:
                pass
            self.setCellTracking(True)
        elif col == BillTableColumn.Qnty:  # Change in Quantity Column
            logging.debug(f"Cell change in Quantity column at row={row}")
            try:
                self.setCellTracking(False)
                Quantity = self.getText(row, BillTableColumn.Qnty, int)
                Rate = self.getText(row, BillTableColumn.Rate, float)
                Price = Quantity * Rate
                try:
                    Discount_prct = self.getText(row, BillTableColumn.Disc_prcnt, float)
                    Discount = Price * (Discount_prct / 100)
                    Net_Price = Price - Discount
                    self.setBillColumn(row, BillTableColumn.Price, Net_Price)
                    self.setBillColumn(row, BillTableColumn.Disc, round(Discount, 2))
                except Exception as e:
                    logging.error(f"Error calculating discount percent at row={row}: {e}", exc_info=True)
                    Discount = self.getText(row, BillTableColumn.Disc, float)
                    Net_Price = Price - Discount
                    self.setBillColumn(row, BillTableColumn.Price, Net_Price)
                    Discount_prct = Discount * 100 / Net_Price
                    self.setBillColumn(
                        row, BillTableColumn.Disc_prcnt, round(Discount_prct, 2)
                    )  # Should be verifiedd
                press(["down"] + ["left"] * 3)
                self.setCellTracking(True)
            except Exception as e:
                logging.error(f"Exception in quantity column change at row={row}: {e}", exc_info=True)
        elif col == BillTableColumn.Disc_prcnt:  # Change in Discount Percent
            logging.debug(f"Cell change in Discount Percent column at row={row}")
            try:
                self.setCellTracking(False)
                try:
                    Discount_Percentage = self.getText(row, BillTableColumn.Disc_prcnt, float)
                except ValueError:
                    Discount_Percentage = 0
                    self.setBillColumn(row, col, 0)
                Quantity = self.getText(row, BillTableColumn.Qnty, int)
                Rate = self.getText(row, BillTableColumn.Rate, float)
                Price = Quantity * Rate
                Discount = Price * (Discount_Percentage / 100)
                Price_disc = Price - Discount
                self.setBillColumn(row, BillTableColumn.Price, Price_disc)
                self.setBillColumn(row, BillTableColumn.Disc, round(Discount, 2))
                self.setCellTracking(True)
            except Exception as e:
                logging.error(f"Exception in discount percent column change at row={row}: {e}", exc_info=True)
        elif col == BillTableColumn.Disc:  # Change in Discount price
            logging.debug(f"Cell change in Discount column at row={row}")
            try:
                self.setCellTracking(False)
                try:
                    Discount = self.getText(row, BillTableColumn.Disc, float)
                except ValueError:
                    Discount = 0
                    self.setBillColumn(row, col, 0)
                Quantity = self.getText(row, BillTableColumn.Qnty, int)
                Rate = self.getText(row, BillTableColumn.Rate, float)
                Price = Quantity * Rate
                Price_disc = Price - Discount
                self.setBillColumn(row, BillTableColumn.Price, Price_disc)
                Disc_perc = (Discount / Price) * 100
                self.setBillColumn(row, BillTableColumn.Disc_prcnt, round(Disc_perc, 2))
                self.setCellTracking(True)
            except Exception as e:
                logging.error(f"Exception in discount column change at row={row}: {e}", exc_info=True)
        elif col == BillTableColumn.Rate:  # Change in rate column
            logging.debug(f"Cell change in Rate column at row={row}")
            try:
                self.setCellTracking(False)
                Rate = self.getText(row, BillTableColumn.Rate, float)
                Quantity = self.getText(row, BillTableColumn.Qnty, int)
                Price = Quantity * Rate
                Discount = self.getText(row, BillTableColumn.Disc_prcnt, float)
                Disc_Price = Price * Discount / 100
                self.setBillColumn(row, BillTableColumn.Rate, Rate)
                self.setBillColumn(row, BillTableColumn.Disc, round(Disc_Price, 2))
                self.setBillColumn(row, BillTableColumn.Price, round((Price - Disc_Price), 2))
                self.setCellTracking(True)
            except Exception as e:
                logging.error(f"Exception in rate column change at row={row}: {e}", exc_info=True)
                self.setCellTracking(True)
        elif col == BillTableColumn.Name:  # Change in Name column
            logging.debug(f"Cell change in Name column at row={row}")
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
            except Exception as e:
                logging.error(f"Exception in name column change at row={row}: {e}", exc_info=True)
            self.setCellTracking(True)

        try:  # Net Totals and discounts calculation
            self.CalcTotal()
            logging.info(f"Totals and discounts recalculated after cell change at row={row}, col={col}")
        finally:
            self.setCellTracking(True)
        logging.info(f"BMS_Home_GUI.handle_cell_change completed for row={row}, col={col}")

    def CalcTotal(self):
        logging.info("CalcTotal: Calculation started.")
        global total
        net_total = int()
        total = float()
        discount = float()
        dsc_list: list[int | float] = []
        qnty_list: list[int] = []
        try:
            self.setCellTracking(False)
            for key in Bill.getCart():
                curRow = Bill.getRowNumber(key)
                try:
                    total += self.getText(curRow, BillTableColumn.Price, float)
                except Exception as e:
                    logging.error(f"CalcTotal: Error getting price for row={curRow}: {e}", exc_info=True)
                try:
                    disc = self.getText(curRow, BillTableColumn.Disc, float)
                    discount += disc
                    dsc_list.append(disc)
                except Exception as e:
                    logging.error(f"CalcTotal: Error getting discount for row={curRow}: {e}", exc_info=True)
                try:
                    qnty = self.getText(curRow, BillTableColumn.Qnty, int)
                    qnty_list.append(qnty)
                except Exception as e:
                    logging.error(f"CalcTotal: Error getting quantity for row={curRow}: {e}", exc_info=True)
        except Exception as e:
            logging.error(f"CalcTotal: Exception during calculation: {e}", exc_info=True)
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
        logging.info(f"CalcTotal: Calculation complete. total={total}, net_total={net_total}, discount={discount}")
        return {
            "total": total,
            "net_Total": total + discount,
            "discount": discount,
            "dsc_list": dsc_list,
            "qnty_list": qnty_list,
        }

    def getItemList(self) -> list[dict[str, str | int | float]]:
        res: list[dict[str, str | int | float]] = []
        for key in Bill.getCart():
            curROW = Bill.getRowNumber(key)
            name = self.getText(curROW, BillTableColumn.Name)
            if name != "":
                quantity = self.getText(curROW, BillTableColumn.Qnty)
                rate = self.getText(curROW, BillTableColumn.Rate)
                amount = round(int(quantity) * float(rate), 2)
                res.append(
                    {
                        "name" : name,
                        "rate" : float(rate),
                        "qty" : int(quantity),
                        "amount" : float(amount)
                    }
                )
        return res

    def log_bill(self):
        logging.info("log_bill called.")
        if Bill.isEmpty():
            logging.info("No items in bill. log_bill exiting early.")
            return
        try:
            final = self.CalcTotal()
            discount = float(final.get("discount", 0))
            nettotal = float(final.get("net_Total", 0))
            logging.info(f"Totals calculated: nettotal={nettotal}, discount={discount}")

            # Define the content of your bill
            company_name = "Fashion Paradise"
            address1 = "No. 1, Richwood Avenue, Market Road,"
            address2 = "Thaiyur - 603 103."
            bill_number = Bill.Get_Bill_No()
            bill_date = date.today().strftime("%d.%m.%Y")
            bill_time = datetime.now().time().strftime("%H:%M:%S")
            billed_by = "{} ({})".format(*User.getNameDesignation())
            logging.info(f"Generating bill: number={bill_number}, date={bill_date}, time={bill_time}, billed_by={billed_by}")
            printer.print_receipt(
                store_name=company_name,
                address_lines= [address1, address2],
                bill_no=bill_number,
                billed_by=billed_by.split()[0],
                items=self.getItemList(), #TODO
                total=nettotal,
                discount=discount,
                net_total= nettotal - discount
            )
            # Set the font and font size
            font_name = "Helvetica"
            font_size = 10
            line_height = font_size * 1.2

            # Calculate the height of the content
        # content_height = 1.7 * inch + line_height * len(bill_data) + 0.8 * inch#-.05
            content_height = 11.9 * inch
        # Create a new canvas with a page size of 3 inches wide and dynamic height
            pdf_path = pathJoiner("Bills", f"{bill_number}.pdf")
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
            for key in Bill.getCart():
                curROW = Bill.getRowNumber(key)
                name = self.getText(curROW, BillTableColumn.Name)
                if name != "":
                    quantity = self.getText(curROW, BillTableColumn.Qnty)
                    rate = self.getText(curROW, BillTableColumn.Rate)
                    amount = round(int(quantity) * float(rate), 2)
                    c.drawString(0.17 * inch, y, str(sno))
                    c.drawString(0.48 * inch, y, name[:22])
                    c.drawString(1.77 * inch, y, rate)
                    c.drawString(2.18 * inch, y, quantity)
                    c.drawString(2.57 * inch, y, str(amount))
                    self.resetRow(curROW)
                    y -= line_height
                    sno += 1
                else:
                    self.resetRow(curROW)
        # Add total and net total
            c.setFont('Helvetica', font_size + 1)
            c.drawString(1 * inch, y - 0.15 * inch, f"Total        : Rs. {str(round(nettotal, 2))}")
            c.drawString(1 * inch, y - 0.35 * inch, f"Discount  : Rs. {str(discount)}")
            c.setFont('Helvetica-Bold', font_size + 1)
            c.drawString(1 * inch, y - 0.55 * inch, f"Net Total : Rs. {str(round(nettotal-discount, 2))}/-")

        # Save the canvas to generate the PDF file
            c.save()
            logging.info(f"PDF bill saved to {pdf_path}")
            location = abspath(pathJoiner(DIREC, "Bills", f"{bill_number}.pdf"))
            try:
                if CURR_PLATFORM == 'Windows':
                    ShellExecute(0, "print", location, None, ".", 0)  # type: ignore
                elif CURR_PLATFORM == 'Linux':
                    subprocess.run(['lpr', location])
                else:
                    raise Exception(f"Unsupported platform: {CURR_PLATFORM}")
                logging.info(f"Sent bill PDF to printer: {location}")
            except Exception as e:
                logging.error(f"Error printing bill PDF: {e}", exc_info=True)
            items_qry_data = {
                "bill_no": bill_number,
                "date": date.today().strftime("%d.%m.%Y")
                + ", "
                + datetime.now().time().strftime("%H:%M:%S"),
                "items": list(Bill.getCartItems()),
                "discounts": final["dsc_list"],
                "quantity": final["qnty_list"],
                "total": round(nettotal - discount, 2),
            }
            logging.info(f"Posting bill data to API: {items_qry_data}")
            json_data = dumps(items_qry_data)
            try:
                post(f"{url}//bills", json=json_data)
                logging.info("Bill data posted to API successfully.")
            except Exception as e:
                logging.error(f"Error posting bill data to API: {e}", exc_info=True)
            Bill.nextBillPrep()
            self.CalcTotal()
            self.setup(init=True)
            logging.info("log_bill completed successfully.")
        except Exception as e:
            logging.error(f"Exception in log_bill: {e}", exc_info=True)


    def logout(self):
        logging.info("logout: Initiating logout process.")
        confirmation_dialog = QMessageBox(self)
        confirmation_dialog.setWindowTitle("Confirmation")
        confirmation_dialog.setText("Are you sure you want to logout?")
        confirmation_dialog.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        confirmation_dialog.setIcon(QMessageBox.Icon.Question)
        reply = confirmation_dialog.exec()
        if reply == QMessageBox.StandardButton.Yes:
            logging.info("logout: User confirmed logout. Logging out...")
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
            logging.info("logout: Logout completed. Application closed.")
            exit(True)
        else:
            logging.info("logout: Logout cancelled by user.")
            return


def starter():
    logging.info("Script entry point reached.")
    try:
        Init()
    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True)
        exi(1)
    logging.info("Script finished execution.")

if __name__ == "__main__":
    starter()
