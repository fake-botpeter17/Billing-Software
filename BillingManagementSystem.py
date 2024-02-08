from psycopg2 import *
#import pandas
#from tkinter import *
#def authentication():
#def Billing():
#def Stock():
#def Stock_Update():
#def Search():
from time import sleep
from math import * 

def Init():
    con=connect()
    cur = con.cursor()
def Home():
    Uid=input("Enter User ID:")
    Pwd=input("Enter Password:")
    if Auth(Uid,Pwd):
        #Menu
        #Try Different Menus for Admin and User
    print("Wrong password")  #STOPPED HERE       

    return 0
def Auth(a,b):
    cur.execute("select * from users")
    check=cur.fetchall()
    for  i in check:
        if i[0]==i[1]:
            return True
    return False

