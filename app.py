from flask import Flask, jsonify, request
from pymongo import MongoClient
from os import getenv as cred_
from urllib.parse import quote_plus
from pickle import load
from bcrypt import hashpw, gensalt

def cred(attr :str, parse :bool = False) -> str | None:
    """Returns the value of the environment variable with the given name."""
    if not parse:
        return cred_(attr)
    env = cred_(attr)
    if env is not None:
        return quote_plus(env)
    return None

app = Flask(__name__)

try:
    url = cred("Mongo_Con_Str")
    if url is None:
        raise ValueError("URL")
    client = MongoClient(eval(url))
    db_name = cred("Mongo_DB")
    if db_name is None:
        raise ValueError("DB")
    db = client[db_name]
except ValueError as ve:
    reason = ve.args
    print(f"{ve} ({reason})")

BMS = client['BMS']
users_table = BMS['users']
items_table = BMS['items']

@app.route('/items/<int:item_id>',methods = ['GET'])
def get_item(item_id :int):
    item = items_table.find_one({'id':item_id},{'_id':False, 'added':False, 'id': False, 'cp':False, 'qnty':False})
    if item is None:
        return jsonify(None)
    return jsonify(item), 200

@app.route('/authenticate/<string:user_id>/<string:password>',methods = ['GET'])
def authenticate(user_id :str, password :str):
    result = users_table.find_one({'uid':user_id},{'_id':False,'uid':False})
    print(result)
    if result is None:
        return jsonify(None)
    try:
        with open("BillingInfo.dat",'rb+') as f:
           data = load(f)
    except FileNotFoundError as fe:
        return jsonify(f"{fe}"),404
    salt :bytes = data[result['salt']]     
    pwd :bytes = hashpw(password.encode(), salt)
    print(pwd,result['hashed_pwd'],sep='\n')
    if str(pwd) == str(result['hashed_pwd']):
        print("Hello")
        return jsonify(result), 200
    return jsonify(None)

@app.route("/connected")
def is_connected():
    return jsonify(client._opened)

if __name__=='__main__':
    app.run(debug=True)