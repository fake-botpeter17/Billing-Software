from psycopg2 import *
from bcrypt import gensalt, hashpw
from pickle import load,dump 
from secrets import token_urlsafe
from os import getenv, path
pathJoiner = path.join
expanduser = path.expanduser

def  SetPassword(Num :int=1,host_ :str= "{}".format(getenv('Database_Host')),Db :str= "{}".format(getenv('Database_Name')),usr :str="{}".format(getenv("Database_User")),pwd :str= "{}".format(getenv('Database_Pwd')),Port :str="{}".format(getenv("Database_Port"))):
    try:
        con=connect(host=host_, database=Db ,user=usr ,password=pwd, port = Port)#Establishing Connection to the Server
    except:
        print("Error! Could not connect to the server!")
        return
    cur=con.cursor()
    f=open(pathJoiner(expanduser("~"), "BillingInfo.dat"), "rb")
    data =load(f)
    query="update users set pwd=%s,hash_key=%s where uid = %s"
    for i in range(Num): 
        hash_id=token_urlsafe(32)
        user=input("Enter the User ID:")
        try:
            cur.execute("select * from users where uid='{}'".format(user))
            d=cur.fetchall()
            if len(d)>0:
                pass
            else:
                print("User ID does not exist!")
                print("Register First!")
                return
        except Exception as e:
            print(f"Error: {e}")
            return
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
    g=open(pathJoiner(expanduser("~"), "BillingInfo.dat"), "wb")
    dump(data,g)
    g.close()

if __name__=='__main__':
    SetPassword()
