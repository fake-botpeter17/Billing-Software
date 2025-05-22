from secrets import token_urlsafe
from psycopg2 import *
from bcrypt import gensalt, hashpw
from pickle import load,dump
from os import getenv, path
pathJoiner = path.join
expanduser = path.expanduser

def  RegisterUser(host_ :str= "{}".format(getenv('Database_Host')),
                  Db :str= "{}".format(getenv('Database_Name')),
                  usr :str="{}".format(getenv("Database_User")),
                  pwd :str= "{}".format(getenv('Database_Pwd')),
                  Port :str="{}".format(getenv("Database_Port"))):
    try:
        con=connect(host=host_, 
                    database=Db ,
                    user=usr ,
                    password=pwd, 
                    port = Port)#Establishing Connection to the Server
    except:
        print("Error! Could not connect to the server!")
        return
    cur=con.cursor()
    f=open(pathJoiner(expanduser("~"), "BillingInfo.dat"), "rb")
    data =load(f)
    f.close()
    valid=False
    while not valid:
        uid=input("Enter a user ID:")
        cur.execute(f"select * from users where uid='{uid}'")
        if cur.fetchone() is not None:
            print("User ID unavailable!")
        else:
            valid=True
    password_temp=input("Enter a password:")
    name=input("Enter your name: ")
    designation=input("Enter your designation: ")
    salt=gensalt()
    hash_id=token_urlsafe(32)
    password=hashpw(password_temp.encode(),salt)
    values= (uid,designation,str(password),hash_id,name)
    cur.execute("insert into users values(%s,%s,%s,%s,%s)",values)
    g=open(pathJoiner(expanduser("~"), "BillingInfo.dat"), "wb")
    data[hash_id]=salt
    dump(data,g)
    g.close()
    con.commit()
    con.close()
    print("User Registered Successfully!")

if __name__=='__main__':
    RegisterUser()
