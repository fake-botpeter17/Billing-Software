import datetime
#import pyarrow
from psycopg2 import *
#import pandas
from random import randint
from tkinter import *
#def authentication():
#def Stock():
#def Stock_Update():
#def Search():
#from math import * 
from time import sleep
def Login():
    login_window=Tk()
    login_window.title("Login")
    login_window.geometry('300x150')
    #login_window.configure(bg='light grey')
    Uid=input("Enter User ID:")
    Pwd=input("Enter Password:")
    if not(Auth(Uid,Pwd)):
        print("Email or password is invalid!")                                      #Displaying  error message when user enters wrong email id/password
        Login()
    login_window.mainloop()
    Menu()      
def Auth(a,b):
    cur.execute("select * from users")
    check=cur.fetchall()
    for  i in check:
        if i[0]==a:
            if i[1]==b:
                if i[2]=="Admin":
                    global Admin
                    Admin=True                                                      #Assigning the role (Admin or not)
                    return True
    return False
def Menu():
    print("1. Billing \n2. Inventory \n3. Stock Management\n 4. Sales Info\n5. Staff Management")
    ch=int(input(f"Please Enter Your Choice (1/2/3/4):"))
    if ch==1:
        Billing()
    elif ch==2:
        Inventory()
    elif ch==3:
        StockMngmnt()
    elif ch==4:
        SalesInfo()
    elif ch==5:
        StaffMngmnt()
    else:
        print("\nInvalid Option!!!\n")
        Menu()

def Billing():
    cust_name=input("Customer Name:")
    billno=randint(0,9999)
    print(f"\nYour Bill Number is {billno}")
    itemcode=input("Item Code:")
    
    qty=int(input("Quantity:")) 
    rate=float(input("Price per Item:"))
    price=qty*rate
    #Should plan
#def Inventory():



con=connect (host='192.168.226.69', database = 'BMS',user = 'postgres',password = 'Nebinson@1', port = '5432')
cur = con.cursor()
Admin=False
bye=False
while not bye:
    Login()