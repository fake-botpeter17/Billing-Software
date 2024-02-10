import datetime
#import pyarrow
from psycopg2 import *
#import pandas
from random import randint
from tkinter import *
from tkinter import messagebox
#def authentication():
#def Stock():
#def Stock_Update():
#def Search():
#from math import * 
from time import sleep

def Login():

    global login_window

    #Init

    login_window=Tk()
    frame=Frame(bg='#333333')
    login_window.title("Login")
    login_window.geometry('550x600')
    login_window.configure(bg='#333333')

    #Widgets

    login_label=Label(frame,text="Login",font=("Helvetica",30),bg='#333333',fg='#FF3399',pady=40)
    username_label=Label(frame,text="Username: ",font=("Helvetica",15),bg='#333333',fg="#FFFFFF")
    password_label=Label(frame,text="Password: ",font=("Helvetica",15),bg='#333333',fg="#FFFFFF")
    username_entry=Entry(frame,font=("Helvetica",15))
    password_entry=Entry(frame,show='*',font=("Helvetica",15))
    login_button=Button(frame,text="Login",command=lambda: Auth(username_entry.get(),password_entry.get()),bg='#ffffff',fg='#FF3399')

    #Displaying

    login_label.grid(row=0,column=0,columnspan=2,sticky='news',pady=40)
    username_label.grid(row=1,column=0)
    username_entry.grid(row=1,column=1,pady=20)
    password_label.grid(row=2,column=0)
    password_entry.grid(row=2,column=1,pady=20)
    login_button.grid(row=3,column=0,columnspan=2,pady=30)
    frame.pack()
    login_window.mainloop()


def Auth(a,b):
    cur.execute("select * from users")
    check=cur.fetchall()
    for  i in check:
        if i[0]==a:
            if i[1]==b:
                global login_window
                if i[2]=="Admin":
                    global Admin
                    Admin=True              #Assigning Roles
                    messagebox.showinfo(title="Successful!",message="You are now logged in as Admin.")
                    login_window.destroy()                                                    
                    Menu()
                messagebox.showinfo(title="Successful!",message="You are now logged in")
                login_window.destroy()
                Menu()
    messagebox.showerror(title= "Error!",message = 'Wrong Username or Password')
def Menu():

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
    
'''
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
'''
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
Login()