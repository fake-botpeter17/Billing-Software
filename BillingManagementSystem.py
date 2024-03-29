'''                 IMPORTS                       '''

from sqlite3 import Row
import subprocess
from time import sleep
from typing import Generator,NoReturn
from psycopg2 import *
from tkinter import Tk,Frame,Label,Entry,Button,messagebox          
from PyQt6.QtWidgets import * 
from PyQt6.QtWidgets import QTableWidget 
from PyQt6.QtGui import QIcon
from PyQt6 import uic
from bcrypt import hashpw
from pickle import load
from datetime import datetime,date
import psycopg2
import UserRegistration
import os
import sys

#Global Declaration
Name_Col,Rate_Col,ID_Col,Qnty_Col,Disc_prcnt_Col,Disc_Col,Price_Col=2,3,1,4,5,6,7
'''
    GUI for Login is implemented using Tkinter
    Rest are expected to be implemented using PyQt6
'''

#  Imports that aren't required (FOR NOW)

'''
    from time import sleep
    
    import pyarrow
    import pandas
    def Stock():
    def Stock_Update():
    def Search():
    from math import * 
'''

User=str()

def Init():
    try:
        con=connect(host="{}".format(os.getenv('Database_Host')), 
                    database = "{}".format(os.getenv('Database_Name')),
                    user = "{}".format(os.getenv("Database_User")),
                    password ="{}".format(os.getenv('Database_Pwd')), 
                    port = "{}".format(os.getenv("Database_Port")))                                 #Establishing Connection to the Server
    except psycopg2.Error as e:
        messagebox.showerror("Authentication Error", "Error connecting to the database server: {}".format(e))
        messagebox.showinfo("Error","Try opening the program as Administrator")
        exit(True)                                                                                                  #Exiting the Prgram when Connection to server failed 
    global cur,Admin
    cur = con.cursor()                                                                                  
    Admin=False
    Login()

'''def My_IP():
    output = subprocess.check_output(["ipconfig", "/all"], universal_newlines=True)
    for line in output.split("\n"):
        if line.startswith("IPv4 Address. . . . . . . . . . . :"):
            ip_address = line.split(":")[1].strip()
            break
    else:
        raise Exception("Failed to find IPv4 address")
    return ip_address
'''

def Profile_(User):
    ...


def main():
    global app
    app = QApplication([])
    window = MyGUI()
    sys.exit(app.exec())


def Bill_Number() -> Generator:
    '''
        Should Update The lower bound every time the program starts (JUST IN CASE)
        Log Bills to DB
    '''
    for i in range(10000,100000):
        yield i

Bill_No :Generator = Bill_Number()                                  #Memory Efficient way to generate bill no. successively (Generator Object)

def Auth(user :str ,pwd :str) -> None :

    '''           Getting Authentication Data from Server                '''
    #############  Should Add a way to save current user #####################
    #############               For displaying in GUI                ############################
    cur.execute("select * from users where uid='{}'".format(user))                                            #Not sure about field Name (PWD & User)
    check :tuple|None=cur.fetchone()                                                        #Column Layout -> [(uid,designation,pwd,salt_id)]
    if check is None:
        messagebox.showerror("Error","User Not found!!")
        return
    '''      Evaluating with respect to the obtained data               '''
    f=open("BillingInfo.dat","rb+")
    data=load(f)
    salt=data[check[-1]]
    password=hashpw(pwd.encode(),salt)
    if str(password)==check[2]:                                                                                                                  #Checking if the Passwords Match
        if check[1].casefold()=="Admin".casefold():
            global Admin
            Admin=True                                                                                                                   #Setting the role as Admin if it is so                                                                         
            messagebox.showinfo(title="Login Successful!",message="You are now logged in as Admin.")
        else:
            messagebox.showinfo(title="Login Successful!",message="You are now logged in.")
        global User
        User=user
        login_window.destroy()                                                                                                  #Closing the Login Window after successful Login                         
        main()                                                                                                                           # Opening Menu after Logging In
            
    else:                                                                                                                  
        messagebox.showerror(title= "Authentication Error!",message = 'Wrong Username or Password')   # Displaying Error if Login Failed
        

def Login() -> None:
    global login_window                                                      #Setting the scope of 'login_window' to GLOBAL

    '''                     Init                    '''
        
    login_window=Tk()
    frame=Frame(bg='#333333')
    login_window.title("Login")
    login_window.geometry('550x600')
    login_window.configure(bg='#333333')

    '''                     Widgets            '''
        
    login_label=Label(frame,text="Login",font=("Helvetica",30),bg='#333333',fg='#FF3399',pady=40)
    username_label=Label(frame,text="Username: ",font=("Helvetica",15),bg='#333333',fg="#FFFFFF")
    password_label=Label(frame,text="Password: ",font=("Helvetica",15),bg='#333333',fg="#FFFFFF")
    username_entry=Entry(frame,font=("Helvetica",15))
    password_entry=Entry(frame,show='*',font=("Helvetica",15))                  #Setting the input type to password (masking with '*')
    login_button=Button(frame,text="Login",command=lambda: Auth(username_entry.get(),password_entry.get()),bg='#ffffff',fg='#FF3399')

    '''       Setting Layout and Displaying         '''

    login_label.grid(row=0,column=0,columnspan=2,sticky='news',pady=40)
    username_label.grid(row=1,column=0)
    username_entry.grid(row=1,column=1,pady=20)
    password_label.grid(row=2,column=0)
    password_entry.grid(row=2,column=1,pady=20)
    login_button.grid(row=3,column=0,columnspan=2,pady=30)

    '''      Packing and Starting Mainloop     '''

    frame.pack()
    login_window.mainloop()



class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI,self).__init__()
        uic.loadUi("Menu.ui", self)
        aspect_ratio = 16/9  # Common aspect ratio for 720p
        min_height = 720
        min_width = int(min_height * aspect_ratio)
        self.setMinimumSize(min_width,min_height)
        self.setWindowTitle("BMS -botpeter17")
        icon=QIcon("My_Icon.jpeg")
        self.setWindowIcon(icon)
        if Admin:
            self.menuSales.setEnabled(True)
            self.menuStock.setEnabled(True)
            self.New_Bill_Tab.setEnabled(True)                             #Should Set back to Flase at exit
        self.show()
        self.Bill_Number_Label.setText("Bill No    : {}".format(next(Bill_No)))
        self.Bill_Date_Label.setText("Bill Date : {}".format(date.today().strftime("%B %d, %Y")))
        self.Billed_By_Label.setText("Billed By : {}".format(User))
        self.Bill_Time_Label.setText("Bill Time :{}".format(datetime.now().time().strftime("%H:%M:%S")))
        self.actionLogout.triggered.connect(lambda: self.logout())   
        self.Profile.triggered.connect(lambda: Profile_(User))
        self.Bill_Table.setColumnCount(8)
        self.Bill_Table.setRowCount(18)
        self.Bill_Table.cellChanged.connect(self.handle_cell_change)
    
    def Data_Input(self):
        ...
    def handle_cell_change(self, row, col):
        """
  This slot function is called when a cell value in the Bill_Table changes.

  Args:
      row (int): The row index of the changed cell.
      col (int): The column index of the changed cell.
        """
         # Access and use the row and col values here
        print(f"Cell at row {row}, column {col} changed!")
        if row is not None:
            if col==ID_Col:
                self.Bill_Table.cellChanged.disconnect(self.handle_cell_change)
                Item_ID=self.Bill_Table.item(row,1).text()
                try:
                    cur.execute("select name,rate from items where id='{}'".format(Item_ID))
                    data=cur.fetchone()
                    if data is not None:
                        Item_Name, Item_Rate = data
                        self.Bill_Table.setItem(row, Name_Col, QTableWidgetItem(Item_Name))  # Set item in table
                        self.Bill_Table.setItem(row, Rate_Col, QTableWidgetItem(str(Item_Rate)))  # Set item in 
                        self.Bill_Table.setItem(row,0,QTableWidgetItem(str(row+1)))
                        self.Bill_Table.setItem(row,Disc_prcnt_Col,QTableWidgetItem(str(0)))
                        self.Bill_Table.setItem(row,Disc_Col,QTableWidgetItem(str(0)))
                        self.Bill_Table.setItem(row,Qnty_Col,QTableWidgetItem(str(1)))
                        self.Bill_Table.setItem(row,Price_Col,QTableWidgetItem(str(Item_Rate)))
                except:
                    pass
                self.Bill_Table.cellChanged.connect(self.handle_cell_change)
            elif col==Qnty_Col:
                try:
                    self.Bill_Table.cellChanged.disconnect(self.handle_cell_change)
                    Quantity=int(self.Bill_Table.item(row,4).text())
                    Rate=int(self.Bill_Table.item(row,3).text())
                    Price=Quantity*Rate
                    self.Bill_Table.setItem(row,Price_Col,QTableWidgetItem(str(Price)))
                    self.Bill_Table.cellChanged.connect(self.handle_cell_change)
                except:
                    pass
            elif col==Disc_prcnt_Col:
                try:
                    self.Bill_Table.cellChanged.disconnect(self.handle_cell_change)
                    Discount_Percentage=int(self.Bill_Table.item(row,col).text())
                    Quantity=int(self.Bill_Table.item(row,4).text())
                    Rate=int(self.Bill_Table.item(row,3).text())
                    Price=Quantity*Rate
                    Discount=Price*(Discount_Percentage/100)
                    Price_disc=Price-Discount
                    self.Bill_Table.setItem(row,Price_Col,QTableWidgetItem(str(Price_disc)))
                    self.Bill_Table.setItem(row,Disc_Col,QTableWidgetItem(str(Discount)))
                    self.Bill_Table.cellChanged.connect(self.handle_cell_change)
                except:
                    pass
            elif col==Disc_Col:
                try:
                    self.Bill_Table.cellChanged.disconnect(self.handle_cell_change)
                    Discount=int(self.Bill_Table.item(row,col).text())
                    Quantity=int(self.Bill_Table.item(row,4).text())
                    Rate=int(self.Bill_Table.item(row,3).text())
                    Price=Quantity*Rate
                    Price_disc=Price-Discount
                    self.Bill_Table.setItem(row,Price_Col,QTableWidgetItem(str(Price_disc)))
                    Disc_perc=((Discount/Price)*100)
                    self.Bill_Table.setItem(row,Disc_prcnt_Col,QTableWidgetItem(str(Disc_perc)))
                    self.Bill_Table.cellChanged.connect(self.handle_cell_change)
                except:
                    pass

                            
    def logout(self):
        confirmation_dialog = QMessageBox(self)
        confirmation_dialog.setWindowTitle("Confirmation")
        confirmation_dialog.setText("Are you sure you want to logout?")
        confirmation_dialog.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        confirmation_dialog.setIcon(QMessageBox.Icon.Question)
        reply=confirmation_dialog.exec()
        if reply==QMessageBox.StandardButton.Yes:
            Admin=False
            self.menuSales.setEnabled(False)
            self.menuStock.setEnabled(False)
            self.New_Bill_Tab.setEnabled(False)
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




'''
def Menu() -> None:

    #GUI Init

    global menu_window
    menu_window=Tk()
    menu_window.title("Menu")
    menu_window.geometry('700x800')
    menu_window.configure(bg='#FDFEFE')

    #Widgets

    menu_label=Label(menu_window,text="Menu",font=("Helvetica",30),bg='#333333',fg='#FF3399')
    Billing_button=Button(menu_window,text="Billing System",command=lambda : Billing(),bg="#6A5ACD",activebackground="#4B40BD",fg='white')
    Inventory_button=Button(menu_window,text="Inventory",command=lambda :Inv(), bg="#6A5ACD",activebackground="#4B40BD",fg='white')
    StockMng_button=Button(menu_window,text="Stock Management",command=lambda :StockManagement(),bg="#6A5ACD",activebackground="#4B40BD",fg='white')
    SalesInfo_Button=Button(menu_window,text="Sales Information",command=lambda : Sales(), bg="#6A5ACD",activebackground="#4B40BD",fg='white')
    StaffInfo_Button=Button(menu_window,text="Staff Information",command=lambda :StaffInfo(), bg="#6A5ACD",activebackground="#4B40BD",fg='white')
    Logout_Button=Button(menu_window,text="Log Out",command=lambda : [LogOut(),menu_window.destroy()],font=("Helvetica",15))

    #Displaying
        
    menu_label.grid(row=0,column=0,columnspan=2,sticky='news',pady=40)
    Billing_button.grid(row=1,column=0,padx=65)
    Inventory_button.grid(row=1,column=1,padx=65)
    StockMng_button.grid(row=2,column=0,padx=65)
    SalesInfo_Button.grid(row=2,column=1,padx=65)
    StaffInfo_Button.grid(row=3,column=0,columnspan=2,pady=20)
    Logout_Button.grid(row=4,column=0,columnspan=2,pady=10)
    menu_window.mainloop()

def Billing() -> None:
    cust_name=input("Customer Name:")
    billno=next(Bill_No)
    print(f"\nYour Bill Number is {billno}")
    itemcode=input("Item Code:")
    qty=int(input("Quantity:")) 
    rate=float(input("Price per Item:"))
    price=qty*rate
    #Should plan
    #def Inventory():

    '''

Init()