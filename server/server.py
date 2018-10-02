from flask import Flask, request, redirect, jsonify
from database.manager import dbManager
from consts import Consts
from log.logger import Logger
import json

app = Flask(__name__)
db = dbManager.instance()

@app.route('/idcheck', methods = ['POST', 'GET'])
def idcheck():
    data = request.form.to_dict()
    if db.id_check(data) == '1':
        return '1'
    else:
        return '0'

@app.route('/login', methods = ['POST', 'GET']) # id, password
def login():
    data = request.form.to_dict()
    try:
        return json.dumps(db.login(data), ensure_ascii = False)
    except:
        return json.dumps({'error' : Consts.DB_ERROR.value}, ensure_ascii = False)

@app.route('/signin', methods = ['POST', 'GET'])
def signIn():
    data = request.form.to_dict()
    try:
        return json.dumps(db.signIn(data), ensure_ascii = False)
    except:
        return json.dumps({'error' : Consts.DB_ERROR.value}, ensure_ascii = False)

@app.route('/search_bar', methods = ['POST', 'GET'])
def search_bar():
    data = request.form.to_dict()
    return json.dumps(db.search_bar(data), ensure_ascii = False)

@app.route('/cosmetic_info', methods = ['POST', 'GET'])
def get_cosmetic_info():
    data = request.form.to_dict()
    return json.dumps(db.get_cosmetic_info(data), ensure_ascii = False)

@app.route('/get_simple', methods = ['POST', 'GET'])
def get_simple_review():
    data = request.form.to_dict()
    return json.dumps(db.get_simple_review(data), ensure_ascii = False)

@app.route('/get_user', methods = ['POST', 'GET'])
def get_user_info():
    data = request.form.to_dict()
    return json.dumps(db.get_user_info(data), ensure_ascii = False)

def start_test_server():
    app.run('0.0.0.0',debug = True)
