'''                 IMPORTS                       '''

from typing import Generator,NoReturn
from psycopg2 import *
from tkinter import Tk,Frame,Label,Entry,Button,messagebox          
from PyQt6.QtWidgets import *  
from PyQt6 import uic


'''
    GUI for Login is implemented using Tkinter
    Rest are expected to be implemented using PyQt6
'''

#  Imports that aren't required (FOR NOW)

'''
    from time import sleep
    import datetime
    import pyarrow
    import pandas
    def authentication():
    def Stock():
    def Stock_Update():
    def Search():
    from math import * 
'''

class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI,self).__init__()
        uic.loadUi("Menu.ui", self)
        self.show()                   


def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()

if __name__=='__main__':
    main()

def Bill_Number() -> Generator:
    '''
        Should Update The lower bound every time the program starts (JUST IN CASE)
    '''
    for i in range(10021,99999):
        yield i

Bill_No :Generator = Bill_Number()                                  #Memory Efficient way to generate bill no. successively (Generator Object)

def Auth(a :str ,b :str) -> None :

    '''           Getting Authentication Data from Server                '''
    #############  Should Add a way to save current user #####################
    #############               For displaying in GUI                ############################
    cur.execute("select pwd from users where user={}".format(a))                                            #Not sure about field Name (PWD & User)
    check=cur.fetchone()

    '''      Evaluating with respect to the obtained data               '''

    if b==check[0][1]:                                                                                                                  #Checking if the Passwords Match
        if check[0][2].casefold()=="Admin".casefold():
            global Admin
            Admin=True                                                                                                                   #Setting the role as Admin if it is so                                                                         
            messagebox.showinfo(title="Login Successful!",message="You are now logged in as Admin.")
        else:
            messagebox.showinfo(title="Login Successful!",message="You are now logged in.")
        login_window.destroy()                                                                                                  #Closing the Login Window after successful Login                         
        Menu()                                                                                                                           # Opening Menu after Logging In
            
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


try:
    con=connect(host='192.168.226.69', database = 'BMS',user = 'postgres',password = 'Nebinson@1', port = '5432')#Establishing Connection to the Server
except:
    messagebox.showerror("Authentication Error","Server not reachable!")
    exit(True)                                                                                                  #Exiting the Prgram when Connection to server failed 

cur = con.cursor()                                                                                  
Admin=False
Login()

if __name__=="__main__":
    ...