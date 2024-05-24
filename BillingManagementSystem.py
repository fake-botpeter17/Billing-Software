'''                 IMPORTS                       '''

from typing import Generator
from psycopg2 import *
from tkinter import Tk,Frame,Label,Entry,Button,messagebox          
from PyQt6.QtWidgets import * 
from PyQt6.QtWidgets import QTableWidget 
from PyQt6.QtGui import QIcon
from PyQt6 import uic
from PyQt6.QtCore import Qt
from bcrypt import hashpw
from pickle import load
from datetime import datetime,date
from urllib import request
import psycopg2
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
    import UserRegistration
    from time import sleep
    import subprocess
    import pyarrow
    import pandas
    from math import * 
'''

User=str()                  #Stores the current user info
bill_data=dict()           #Acts as temp for Current Bill items
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
        messagebox.showerror("Connection Error", "Error connecting to the Server!!\n\nTry opening the program as Administrator")
        exit(True)
    global cur,Admin
    cur = con.cursor()                                                                                  
    Admin=False
    Login()

@atexit.register
def closure():
    try:
        if not(cur.closed):
            con.close()
    except:
        pass
    global Admin
    Admin=False

def check_Internet() -> bool:
    try:
        request.urlopen('https://www.google.com')
        return True
    except:
        return False
    

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
    
    global cur
    cur.execute("SELECT * FROM bills ORDER BY bill_no DESC LIMIT 1")
    Latest_Bill=cur.fetchone()
    if Latest_Bill is None:
        Latest_Bill_No=10000
    else:
        Latest_Bill_No=Latest_Bill[0]
    for Bill_Number in range(Latest_Bill_No+1,100000):
        yield Bill_Number

Bill_No_Gen :Generator = Bill_Number()                              #Memory Efficient way to generate bill no. successively (Generator Object)
Bill_No=int()
def Auth(user :str ,pwd :str) -> None :

    '''           Getting Authentication Data from Server                '''

    cur.execute("select * from users where uid='{}'".format(user))          
    '''
import pickle
def Init():
    f=open("Bott.dat","wb")
    query={1:"select {} from {} where {}={}"}
    pickle.dump(query,f)
    f.close()
def Query_User():
    f=open("Bott.dat","rb")    -> Bott.dat => Dict of queries
    queries=pickle.load(f)
    print(queries[1].format("*","Student Details","Last Name","N"))

    

OUTPUT:

    select * from Student Details where Last Name=N

    '''                                  
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
        global Bill_No
        Bill_No=next(Bill_No_Gen)
        super(BMS_Home_GUI,self).__init__()
        uic.loadUi("BMS_Home_GUI.ui", self)
        aspect_ratio = 16/9  # aspect ratio 
        min_height = 900
        min_width = int(min_height * aspect_ratio)
        self.setMinimumSize(min_width,min_height)
        self.setWindowTitle("BMS -botpeter17")
        icon=QIcon("My_Icon.ico")
        self.setWindowIcon(icon)
        if Admin:
            self.menuSales.setEnabled(True)
            self.menuStock.setEnabled(True)
            self.New_Bill_Tab.setEnabled(True)                             #Should Set back to Flase at exit
        self.show()
        self.setup()
    def setup(self):
        global Bill_No
        self.Bill_Number_Label.setText("Bill No    : {}".format((Bill_No)))
        self.Bill_Date_Label.setText("Bill Date : {}".format(date.today().strftime("%B %d, %Y")))
        self.Billed_By_Label.setText("Billed By : {}".format(User))
        self.Bill_Time_Label.setText("Bill Time :{}".format(datetime.now().time().strftime("%H:%M:%S")))
        self.actionLogout.triggered.connect(lambda: self.logout())   
        self.Profile.triggered.connect(lambda: Profile_(User))        # Should Change after defining Profile GUI
        self.Bill_Table.setColumnCount(8)
        self.Bill_Table.setRowCount(18)
        self.Bill_Table.cellChanged.connect(self.handle_cell_change)
        self.Print_Button.clicked.connect(self.log_bill)           #######################
        #Setting Column Widths
        #Didn't define the width of price col to allow resizing
        self.Bill_Table.setColumnWidth(0, 100)
        self.Bill_Table.setColumnWidth(ID_Col,150)
        self.Bill_Table.setColumnWidth(Name_Col,350)
        self.Bill_Table.setColumnWidth(Rate_Col,150)
        self.Bill_Table.setColumnWidth(Qnty_Col,150)
        self.Bill_Table.setColumnWidth(Disc_prcnt_Col,175)
        self.Bill_Table.setColumnWidth(Disc_Col,175)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Exit?',
                                     "Are you sure you want to quit?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            global Admin
            Admin = False
            try:
                global con
                con.close()
            except:
                pass
            event.accept()  
        else:
            event.ignore() 

    def handle_cell_change(self, row, col):
        if row is not None:
            if col==ID_Col:       #Change in ID Column
                self.Bill_Table.cellChanged.disconnect(self.handle_cell_change)
                try:      #Checking if the ID is entered or deleted
                    s=self.Bill_Table.item(row,1).text()
                    Item_ID=int(s)
                    try:   #IF entered, Aligning it to the center
                        item=QTableWidgetItem(s)
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.Bill_Table.setItem(row,ID_Col,item)
                    except:
                        pass

                except:    #If ID is not readable, checking if it was removed
                    if self.Bill_Table.item(row,ID_Col).text()=="" or self.Bill_Table.item(row,ID_Col).text()==None:
                        item=QTableWidgetItem("")   #IF removed, setting back to defaults
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.Bill_Table.setItem(row,0,item)
                        item=QTableWidgetItem("")
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.Bill_Table.setItem(row,Name_Col,item)
                        item=QTableWidgetItem("")
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.Bill_Table.setItem(row,Rate_Col,item)
                        item=QTableWidgetItem("")
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.Bill_Table.setItem(row,Qnty_Col,item)
                        item=QTableWidgetItem("")
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.Bill_Table.setItem(row,Disc_prcnt_Col,item)
                        item=QTableWidgetItem("")
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.Bill_Table.setItem(row,Disc_Col,item)
                        item=QTableWidgetItem("")
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.Bill_Table.setItem(row,Price_Col,item)
                try:      #If ID is entered, Checking if it is in database
                    cur.execute("select name,selling_price from items where id='{}'".format(Item_ID))
                    data=cur.fetchone()
                    if row in bill_data.values():    #Checking if the row is new or is it being updated
                        item=QTableWidgetItem(str(row+1))
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.Bill_Table.setItem(row,0,item)
                        item=QTableWidgetItem('')
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.Bill_Table.setItem(row,Name_Col,item)
                        item=QTableWidgetItem('')
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.Bill_Table.setItem(row,Rate_Col,item)
                        item=QTableWidgetItem(str(1))
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.Bill_Table.setItem(row,Qnty_Col,item)
                        item=QTableWidgetItem(str(0))
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.Bill_Table.setItem(row,Disc_prcnt_Col,item)
                        item=QTableWidgetItem(str(0))
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.Bill_Table.setItem(row,Disc_Col,item)
                        item=QTableWidgetItem(str(0))
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.Bill_Table.setItem(row,Price_Col,item)
                        for key in bill_data.keys():
                            if bill_data[key]==row:
                                break
                        bill_data.pop(key,None)
                            
                    if data is not None:    #If the elemnt is present in the db, proceed
                        if Item_ID in bill_data.keys():
                            item=QTableWidgetItem("")
                            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                            self.Bill_Table.setItem(row,ID_Col,item)
                            row=bill_data[Item_ID]
                            qnty=int(self.Bill_Table.item(row,Qnty_Col).text())
                            item=QTableWidgetItem(str(qnty+1))
                            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                            self.Bill_Table.setItem(row,Qnty_Col,item)
                            try:
                                Quantity=int(self.Bill_Table.item(row,4).text())
                                Rate=int(self.Bill_Table.item(row,3).text())
                                Price=Quantity*Rate
                                item=QTableWidgetItem(str(Price))
                                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                                self.Bill_Table.setItem(row,Price_Col,item)                                
                            except:
                                pass
                            pass
                        else:
                            Item_Name, Item_Rate = data    #Initialising the data received from the DB
                            item=QTableWidgetItem(Item_Name)
                            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                            self.Bill_Table.setItem(row, Name_Col, item)  # Set item in table
                            item=QTableWidgetItem(str(Item_Rate))
                            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                            self.Bill_Table.setItem(row, Rate_Col, item)  # Set item in 
                            item=QTableWidgetItem(str(row+1))
                            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                            self.Bill_Table.setItem(row,0,item)
                            item=QTableWidgetItem(str(0))
                            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                            self.Bill_Table.setItem(row,Disc_prcnt_Col,item)
                            item=QTableWidgetItem(str(0))
                            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                            self.Bill_Table.setItem(row,Disc_Col,item)
                            item=QTableWidgetItem(str(1))
                            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                            self.Bill_Table.setItem(row,Qnty_Col,item)
                            item=QTableWidgetItem(str(Item_Rate))
                            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                            self.Bill_Table.setItem(row,Price_Col,item)
                            bill_data[Item_ID] = row
                    else:
                        if Item_ID in bill_data.keys():
                            item=QTableWidgetItem("")
                            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                            self.Bill_Table.setItem(row,ID_Col,item)
                            row=bill_data[Item_ID]
                            qnty=int(self.Bill_Table.item(row,Qnty_Col).text())
                            item=QTableWidgetItem(str(qnty+1))
                            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                            self.Bill_Table.setItem(row,Qnty_Col,item)
                            try:
                                Quantity=int(self.Bill_Table.item(row,4).text())
                                Rate=int(self.Bill_Table.item(row,3).text())
                                Price=Quantity*Rate
                                item=QTableWidgetItem(str(Price))
                                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                                self.Bill_Table.setItem(row,Price_Col,item)                                
                            except:
                                pass
                            pass
                        else:
                            item=QTableWidgetItem(str(row+1))
                            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                            self.Bill_Table.setItem(row,0,item)
                            item=QTableWidgetItem(str(0))
                            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                            self.Bill_Table.setItem(row,Disc_prcnt_Col,item)
                            item=QTableWidgetItem(str(0))
                            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                            self.Bill_Table.setItem(row,Disc_Col,item)
                            item=QTableWidgetItem(str(1))
                            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                            self.Bill_Table.setItem(row,Qnty_Col,item)
                            bill_data[Item_ID] = row
                except:
                    pass
                self.Bill_Table.cellChanged.connect(self.handle_cell_change)
            elif col==Qnty_Col:        #Change in Quantity Column 
                try:
                    self.Bill_Table.cellChanged.disconnect(self.handle_cell_change)
                    Quantity=int(self.Bill_Table.item(row,Qnty_Col).text())
                    Rate=int(self.Bill_Table.item(row,Rate_Col).text())
                    Price=Quantity*Rate
                    try:
                        Discount_prct=float(self.Bill_Table.item(row,Disc_prcnt_Col).text())
                        Discount=Price*(Discount_prct/100)
                        Net_Price=Price-Discount
                        item=QTableWidgetItem(str(Net_Price))
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.Bill_Table.setItem(row,Price_Col,item)
                        item=QTableWidgetItem(str(round(Discount,2)))
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.Bill_Table.setItem(row,Disc_Col,item)
                    except:
                        Discount=int(self.Bill_Table.item(row,Disc_Col).text())
                        Net_Price=Price-Discount
                        item=QTableWidgetItem(str(Net_Price))
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.Bill_Table.setItem(row,Price_Col,item)
                        Discount_prct=Discount*100/Net_Price
                        item=QTableWidgetItem(str(round(Discount_prct,2)))
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.Bill_Table.setItem(row,Disc_Col,item)
                    self.Bill_Table.cellChanged.connect(self.handle_cell_change)
                except:
                    pass
            elif col==Disc_prcnt_Col:      #Change in Discount Percent 
                try:
                    self.Bill_Table.cellChanged.disconnect(self.handle_cell_change)
                    Discount_Percentage=int(self.Bill_Table.item(row,col).text())
                    Quantity=int(self.Bill_Table.item(row,4).text())
                    Rate=int(self.Bill_Table.item(row,3).text())
                    Price=Quantity*Rate
                    Discount=Price*(Discount_Percentage/100)
                    Price_disc=Price-Discount
                    item=QTableWidgetItem(str(Price_disc))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.Bill_Table.setItem(row,Price_Col,item)
                    item=QTableWidgetItem(str(round(Discount,2)))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.Bill_Table.setItem(row,Disc_Col,item)
                    self.Bill_Table.cellChanged.connect(self.handle_cell_change)
                except:
                    pass
            elif col==Disc_Col:     #Change in Discount price
                try:
                    self.Bill_Table.cellChanged.disconnect(self.handle_cell_change)
                    Discount=int(self.Bill_Table.item(row,col).text())
                    Quantity=int(self.Bill_Table.item(row,4).text())
                    Rate=int(self.Bill_Table.item(row,3).text())
                    Price=Quantity*Rate
                    Price_disc=Price-Discount
                    item=QTableWidgetItem(str(Price_disc))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.Bill_Table.setItem(row,Price_Col,item)
                    Disc_perc=((Discount/Price)*100)
                    item=QTableWidgetItem(str(round(Disc_perc,2)))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.Bill_Table.setItem(row,Disc_prcnt_Col,item)
                    self.Bill_Table.cellChanged.connect(self.handle_cell_change)
                except:
                    pass
            elif col==Rate_Col:      #Change in rate column 
                try:
                    self.Bill_Table.cellChanged.disconnect(self.handle_cell_change)
                    Rate=int(self.Bill_Table.item(row,col).text())
                    Quantity=int(self.Bill_Table.item(row,Qnty_Col).text())
                    Price=Quantity*Rate
                    Discount=int(self.Bill_Table.item(row,Disc_prcnt_Col).text())
                    Disc_Price=Price*Discount/100
                    item=QTableWidgetItem(str(round(Disc_Price,2)))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.Bill_Table.setItem(row,Disc_Col,item)
                    item=QTableWidgetItem(str(round((Price - Disc_Price),2)))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.Bill_Table.setItem(row,Price_Col,item)
                    self.Bill_Table.cellChanged.connect(self.handle_cell_change)
                except:
                    try:
                        self.Bill_Table.cellChanged.connect(self.handle_cell_change)
                        pass
                    except:
                        pass
            global total
            net_total=int()
            total=float()
            discount=float()
            try:                         #Net Totals and discounts calculation
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
                    net_total=round(total+discount,2)
                    self.Total_Label.setText("Total                  : "+str(round(total,2)))
                    self.Net_Total_Label.setText("Net Total          : "+str(net_total))
                    self.Bill_Time_Label.setText("Bill Time :{}".format(datetime.now().time().strftime("%H:%M:%S")))
                    self.Bill_Table.cellChanged.connect(self.handle_cell_change)
            except:
                try:
                    self.Bill_Table.cellChanged.connect(self.handle_cell_change)
                except:
                    pass


    def log_bill(self):
        try:
            if total==0 or total is None:
                return
        except:
            return
        global Bill_No
        with open("Bills//{}.txt".format(Bill_No),'w') as Bill:
            Bill.write(f"{"FASHION PARADISE":^75}")
            Bill.write("\n")
            Bill.write(f"{"No. 1, Richwood Avenue,":^80}")
            Bill.write("\n")
            Bill.write(f"{"Thaiyur Market Road, Kelambakkam, Chennai - 603 103.":^65}")
            Bill.write("\n")
            Bill.write(f"{"~":~^50}")
            Bill.write("\n")
            bn=f"Bill No: {Bill_No}"   #Bill No
            dnt=datetime.now().strftime("%H:%M, %d %B %Y ")
            Bill.write(f"{bn:<{len(bn)}}{'INVOICE':^{73-len(bn)-len(dnt)}}{dnt:>{len(dnt)}}")
            Bill.write("\n")
            Bill.write(f"{"~":~^50}")
            Bill.write("\n")
            Bill.write(f"{"Name":<10}{'Qty':<10}{'Rate':<10}{'Price':<10}{'Discount(%)':<10}{'Discount':<10}{'Net Price':<10}")
            '''
            Should add bill(text) content after determining the Paper size
            Plan Changed

            Using HTML with placeholders for billing
            and then use weasyprint for converting it to pdf and then use jinja for HTML Manipulation
            '''
        ...
        cur.execute("insert into bills values ({},'{}',{},'{}')".format(Bill_No,(date.today().strftime("%d %B, %Y")),total,User))
        con.commit()
        global bill_data
        for key in bill_data.keys(): 
            self.Bill_Table.setItem(bill_data[key],ID_Col,QTableWidgetItem(str()))
        Bill_No=next(Bill_No_Gen)
        bill_data=dict()   #reinitializing the item data stored and hence resetting the Table
        self.setup()
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