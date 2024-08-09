from flask import Flask, jsonify
from pymongo import MongoClient
from pickle import load
from bcrypt import hashpw
from os import getenv as cred

app = Flask(__name__)

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
    if str(pwd) == result['hashed_pwd']:
        return jsonify(result), 200
    return jsonify(None)

@app.route("//get_items")
def get_items():
    res = items_table.find({}, {'_id': False, 'added': False, 'cp': False, 'qnty': False})
    items = []
    for item in res:
        items.append(item)
    return jsonify(items)

@app.route("/connected")
def is_connected():
    return jsonify(client is not None and client.admin.command('ping')['ok'] == 1)
