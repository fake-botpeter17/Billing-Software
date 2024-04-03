'''                 IMPORTS                       '''

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
from urllib import request
import psycopg2
import subprocess
import UserRegistration
import os
import sys
import atexit

#Global Declaration of Column Position
Name_Col,Rate_Col,ID_Col,Qnty_Col,Disc_prcnt_Col,Disc_Col,Price_Col=2,3,1,4,5,6,7

'''
    GUI for Login is implemented using Tkinter
    Rest are expected to be implemented using PyQt6
'''

#  Imports that aren't required (FOR NOW)

'''
    import pyarrow
    import pandas
    from math import * 
'''

User=str()
bill_data=dict()

@atexit.register
def closure():
    try:
        if not(cur.closed):
            con.close()
    except:
        pass
    global Admin
    Admin=False
    
def check_Internet():
    try:
        request.urlopen('https://www.google.com')
        return True
    except:
        return False
    
def Init():
    '''
    Should Change the Logic for checking the Network Connectivity

    Should add a loading Window
    '''
    '''while not(check_Internet()):
        messagebox.showerror("Internet Connection Error", "Please check your internet connection and try again.")
        sleep(5)'''
    try:
        global con
        con=connect(host="{}".format(os.getenv('Database_Host')), 
                    database = "{}".format(os.getenv('Database_Name')),
                    user = "{}".format(os.getenv("Database_User")),
                    password ="{}".format(os.getenv('Database_Pwd')), 
                    port = "{}".format(os.getenv("Database_Port")))                                 #Establishing Connection to the Server
        '''except psycopg2.Error as e:
        messagebox.showerror("Authentication Error", "Error connecting to the database server: {}".format(e))
        messagebox.showinfo("Error","Try opening the program as Administrator")
        exit(True)'''                                                                                                  #Exiting the Prgram when Connection to server failed 
    except:
        messagebox.showerror("Connection Error", "Error connecting to the Server.\nTry opening the program as Administrator")
        exit(True)
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

def main():
    global app
    app = QApplication([])
    window = BMS_Home_GUI()
    sys.exit(app.exec())


def Bill_Number() -> Generator:
    '''
        Should Update The lower bound every time the program starts (JUST IN CASE)   => SELECT * FROM your_table ORDER BY your_primary_key_column DESC LIMIT 1;  
        Query to fetch the last element    ====> 
        ### Should Try getting one arguement as latest bill number and start from it(Lowerbound to that parameter)

        ---------------------------
        def Bill_Number(Latest_Bill_No :int) -> Generator:
            for Bill_Number in range(Latest_Bill_No+1,100000):
                yield Bill_Number
        ---------------------------

        Log Bills to DB
    '''
    for i in range(10000,100000):
        yield i

Bill_No :Generator = Bill_Number()                                  #Memory Efficient way to generate bill no. successively (Generator Object)

def Auth(user :str ,pwd :str) -> None :

    '''           Getting Authentication Data from Server                '''

    cur.execute("select * from users where uid='{}'".format(user))                                            
    check :tuple|None=cur.fetchone()                                                        #Column Layout -> [(uid,designation,pwd,salt_id)]
    if check is None:
        messagebox.showerror("Error","User Not found!!")
        return
    
    '''      Evaluating with respect to the obtained data               '''

    f=open("BillingInfo.dat","rb+")
    data=load(f)
    f.close()
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
    #login_window.overrideredirect(True)     #Removing Close button

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


class BMS_Home_GUI(QMainWindow):
    def __init__(self):
        '''
        Should Set the Column width from code appropriately 
        '''
        super(BMS_Home_GUI,self).__init__()
        uic.loadUi("BMS_Home_GUI.ui", self)
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
        self.Profile.triggered.connect(lambda: Profile_(User))        # Should Change after defining Profile GUI
        self.Bill_Table.setColumnCount(8)
        self.Bill_Table.setRowCount(18)
        self.Bill_Table.cellChanged.connect(self.handle_cell_change)
    
    def handle_cell_change(self, row, col):
        if row is not None:
            if col==ID_Col:
                self.Bill_Table.cellChanged.disconnect(self.handle_cell_change)
                try:
                    Item_ID=int(self.Bill_Table.item(row,1).text())
                except:
                    if self.Bill_Table.item(row,1).text()=="" or self.Bill_Table.item(row,1).text()==None:
                        self.Bill_Table.setItem(row,0,QTableWidgetItem(""))
                        self.Bill_Table.setItem(row,Name_Col,QTableWidgetItem(""))
                        self.Bill_Table.setItem(row,Rate_Col,QTableWidgetItem(""))
                        self.Bill_Table.setItem(row,Qnty_Col,QTableWidgetItem(""))
                        self.Bill_Table.setItem(row,Disc_prcnt_Col,QTableWidgetItem(""))
                        self.Bill_Table.setItem(row,Disc_Col,QTableWidgetItem(str('')))
                        self.Bill_Table.setItem(row,Price_Col,QTableWidgetItem(str("")))
                try:
                    cur.execute("select name,rate from items where id='{}'".format(Item_ID))
                    data=cur.fetchone()
                    if row in bill_data.values():
                        self.Bill_Table.setItem(row,0,QTableWidgetItem(str(row+1)))
                        self.Bill_Table.setItem(row,Name_Col,QTableWidgetItem(''))
                        self.Bill_Table.setItem(row,Rate_Col,QTableWidgetItem(""))
                        self.Bill_Table.setItem(row,Qnty_Col,QTableWidgetItem(str(1)))
                        self.Bill_Table.setItem(row,Disc_prcnt_Col,QTableWidgetItem(str(0)))
                        self.Bill_Table.setItem(row,Disc_Col,QTableWidgetItem(str(0)))
                        self.Bill_Table.setItem(row,Price_Col,QTableWidgetItem(str(0)))
                        for key in bill_data.keys():
                            if bill_data[key]==row:
                                break
                        bill_data.pop(key,None)
                            
                    if data is not None:
                        if Item_ID in bill_data.keys():
                            self.Bill_Table.setItem(row,ID_Col,QTableWidgetItem(""))
                            row=bill_data[Item_ID]
                            qnty=int(self.Bill_Table.item(row,Qnty_Col).text())
                            self.Bill_Table.setItem(row,Qnty_Col,QTableWidgetItem(str(qnty+1)))
                            try:
                                Quantity=int(self.Bill_Table.item(row,4).text())
                                Rate=int(self.Bill_Table.item(row,3).text())
                                Price=Quantity*Rate
                                self.Bill_Table.setItem(row,Price_Col,QTableWidgetItem(str(Price)))                                
                            except:
                                pass
                            pass
                        else:
                            Item_Name, Item_Rate = data
                            self.Bill_Table.setItem(row, Name_Col, QTableWidgetItem(Item_Name))  # Set item in table
                            self.Bill_Table.setItem(row, Rate_Col, QTableWidgetItem(str(Item_Rate)))  # Set item in 
                            self.Bill_Table.setItem(row,0,QTableWidgetItem(str(row+1)))
                            self.Bill_Table.setItem(row,Disc_prcnt_Col,QTableWidgetItem(str(0)))
                            self.Bill_Table.setItem(row,Disc_Col,QTableWidgetItem(str(0)))
                            self.Bill_Table.setItem(row,Qnty_Col,QTableWidgetItem(str(1)))
                            self.Bill_Table.setItem(row,Price_Col,QTableWidgetItem(str(Item_Rate)))
                            bill_data[Item_ID] = row
                    else:
                        if Item_ID in bill_data.keys():
                            self.Bill_Table.setItem(row,ID_Col,QTableWidgetItem(""))
                            row=bill_data[Item_ID]
                            qnty=int(self.Bill_Table.item(row,Qnty_Col).text())
                            self.Bill_Table.setItem(row,Qnty_Col,QTableWidgetItem(str(qnty+1)))
                            try:
                                Quantity=int(self.Bill_Table.item(row,4).text())
                                Rate=int(self.Bill_Table.item(row,3).text())
                                Price=Quantity*Rate
                                self.Bill_Table.setItem(row,Price_Col,QTableWidgetItem(str(Price)))                                
                            except:
                                pass
                            pass
                        else:
                            self.Bill_Table.setItem(row,0,QTableWidgetItem(str(row+1)))
                            self.Bill_Table.setItem(row,Disc_prcnt_Col,QTableWidgetItem(str(0)))
                            self.Bill_Table.setItem(row,Disc_Col,QTableWidgetItem(str(0)))
                            self.Bill_Table.setItem(row,Qnty_Col,QTableWidgetItem(str(1)))
                            bill_data[Item_ID] = row
                except:
                    pass
                self.Bill_Table.cellChanged.connect(self.handle_cell_change)
            elif col==Qnty_Col:
                try:
                    self.Bill_Table.cellChanged.disconnect(self.handle_cell_change)
                    Quantity=int(self.Bill_Table.item(row,Qnty_Col).text())
                    Rate=int(self.Bill_Table.item(row,Rate_Col).text())
                    Price=Quantity*Rate
                    try:
                        Discount_prct=float(self.Bill_Table.item(row,Disc_prcnt_Col).text())
                        Discount=Price*(Discount_prct/100)
                        Net_Price=Price-Discount
                        self.Bill_Table.setItem(row,Price_Col,QTableWidgetItem(str(Net_Price)))
                        self.Bill_Table.setItem(row,Disc_Col,QTableWidgetItem(str(round(Discount,2))))
                    except:
                        Discount=int(self.Bill_Table.item(row,Disc_Col).text())
                        Net_Price=Price-Discount
                        self.Bill_Table.setItem(row,Price_Col,QTableWidgetItem(str(Net_Price)))
                        Discount_prct=Discount*100/Net_Price
                        self.Bill_Table.setItem(row,Discount_Col,QTableWidgetItem(str(round(Discount_prct,2))))
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
                    self.Bill_Table.setItem(row,Disc_Col,QTableWidgetItem(str(round(Discount,2))))
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
                    self.Bill_Table.setItem(row,Disc_prcnt_Col,QTableWidgetItem(str(round(Disc_perc,2))))
                    self.Bill_Table.cellChanged.connect(self.handle_cell_change)
                except:
                    pass
            elif col==Rate_Col:
                try:
                    self.Bill_Table.cellChanged.disconnect(self.handle_cell_change)
                    Rate=int(self.Bill_Table.item(row,col).text())
                    Quantity=int(self.Bill_Table.item(row,Qnty_Col).text())
                    Price=Quantity*Rate
                    Discount=int(self.Bill_Table.item(row,Disc_prcnt_Col).text())
                    Disc_Price=Price*Discount/100
                    self.Bill_Table.setItem(row,Disc_Col,QTableWidgetItem(str(round(Disc_Price,2))))
                    self.Bill_Table.setItem(row,Price_Col,QTableWidgetItem(str(round((Price - Disc_Price),2))))
                    self.Bill_Table.cellChanged.connect(self.handle_cell_change)
                except:
                    try:
                        self.Bill_Table.cellChanged.connect(self.handle_cell_change)
                        pass
                    except:
                        pass

            net_total=int()
            total=float()
            discount=float()
            try:
                for key in bill_data.keys():
                    self.Bill_Table.cellChanged.disconnect(self.handle_cell_change)
                    try:
                        total+=float((self.Bill_Table.item(bill_data[key],Price_Col).text()))
                    except:
                        pass
                    try:
                        discount+=float(self.Bill_Table.item(bill_data[key],Disc_Col).text())
                    except:
                        pass
                    self.Net_Discount_Label.setText("Net Discount    : "+str(round(discount,2)))
                    net_total=(total+discount)
                    self.Total_Label.setText("Total                  : "+str(round(total,2)))
                    self.Net_Total_Label.setText("Net Total          : "+str(net_total))
                    self.Bill_Time_Label.setText("Bill Time :{}".format(datetime.now().time().strftime("%H:%M:%S")))
                    self.Bill_Table.cellChanged.connect(self.handle_cell_change)
            except:
                try:
                    self.Bill_Table.cellChanged.connect(self.handle_cell_change)
                    pass
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
class Profile_GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        '''
        Should create a new .ui File

        Also, should add  User Registration(Adding new User(with every detail) function to the Module
        '''
        ...

'''if __name__=='__main__':
    global Admin
    Admin=True
    main()'''

Init()