from psycopg2 import *
from bcrypt import gensalt, hashpw
from pickle import load,dump 
from secrets import token_urlsafe
import os
def  UserRegistration(Num :int,host_ :str= "{}".format(os.getenv('Database_Host')),Db :str= "{}".format(os.getenv('Database_Name')),usr :str="{}".format(os.getenv("Database_User")),pwd :str= "{}".format(os.getenv('Database_Pwd')),Port :str="{}".format(os.getenv("Database_Port"))):
    try:
        con=connect(host=host_, database=Db ,user=usr ,password=pwd, port = Port)#Establishing Connection to the Server
    except:
        print("Error")
        exit(True)
    cur=con.cursor()
    f=open("E://PETER//BILLING-SOFTWARE//BillingInfo.dat","rb+")
    data =load(f)
    query="update users set pwd=%s,hash_key=%s where uid = %s"
    for i in range(Num): 
        hash_id=token_urlsafe(32)
        user=input("Enter the User ID:")
        pwd=input("Enter the password:")
        salt=gensalt()
        password=hashpw(pwd.encode(),salt)
        values= (str(password),hash_id,user)
        cur.execute(query,values)
        con.commit()
        data[hash_id]=salt
    print("Password Updated Successfully!")
    con.close()
    f.close()
    g=open("E://PETER//BILLING-SOFTWARE//BillingInfo.dat","wb")
    dump(data,g)
    g.close()
