from flask import Flask, jsonify
from pymongo import MongoClient
import os
from pickle import load
from bcrypt import hashpw
from urllib.parse import quote_plus

app = Flask(__name__)

gt = os.environ.copy()
print("GT Dict Copied!!")
DICT_INIT = False

def Init_Dict() -> None:
    global DICT_INIT
    with open("resource.env") as envs:
        envs__ = envs.readlines()
        for line in envs__:
            key, val = line.strip().split('=', maxsplit=1)
            gt[key] = val.strip()
            print(f"Added {key}: {val.strip()}")
    DICT_INIT = True
    print("DICT Initialized with new values!!")

def cred(key: str) -> str | None:
    """Returns the value of the key from the .env file."""
    if not DICT_INIT:
        Init_Dict()
    return gt.get(key)

# Ensure environment variables are initialized before using them
Init_Dict()

url = cred("Mongo_Con_Str")
try:
    client = MongoClient(url)
except Exception as e:
    print(f"Client Init Failed! Error: {e}")

db_name = cred("Mongo_DB")

if db_name is None:
    db_name = "BMS"
BMS = client[db_name]  
users_table = BMS['users']
items_table = BMS['items']

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id: int):
    item = items_table.find_one({'id': item_id}, {'_id': False, 'added': False, 'id': False, 'cp': False, 'qnty': False})
    if item is None:
        return jsonify(None)
    return jsonify(item), 200

@app.route('/authenticate/<string:user_id>/<string:password>', methods=['GET'])
def authenticate(user_id: str, password: str):
    result = users_table.find_one({'uid': user_id}, {'_id': False, 'uid': False})
    if result is None:
        return jsonify(None)
    try:
        with open("BillingInfo.dat", 'rb+') as f:
            data = load(f)
    except FileNotFoundError as fe:
        return jsonify(f"{fe}"), 404
    salt: bytes = data[result['salt']]
    pwd: bytes = hashpw(password.encode(), salt)
    print(pwd, result['hashed_pwd'], sep='\n')
    if pwd == result['hashed_pwd']:
        return jsonify(result), 200
    return jsonify(None)

@app.route("/connected")
def is_connected():
    return jsonify(client is not None and client.admin.command('ping')['ok'] == 1)

@app.route("/test")
def temp():
    return jsonify('Success')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)