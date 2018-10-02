from flask import Flask, request, redirect, jsonify
from database.manager import dbManager
from consts import Consts
from log.logger import Logger
import json

app = Flask(__name__)
db = dbManager.instance()

@app.route('/idcheck', methods = ['POST', 'GET'])
def idcheck():
    if db.idCheck({'id' : request.form[Consts.ID.value]}) == '1':
        return '1'
    else:
        return '0'

@app.route('/login', methods = ['POST', 'GET']) # id, password
def login():
    try:
        return json.dumps(db.login(id = request.form[Consts.ID.value], password = request.form[Consts.PASSWORD.value]), ensure_ascii = False)
    except:
        return json.dumps({'error' : Consts.DB_ERROR.value}, ensure_ascii = False)

@app.route('/signin', methods = ['POST', 'GET'])
def signIn():
    try:
        return json.dumps(db.signIn(id = request.form[Consts.ID.value], password = request.form[Consts.PASSWORD.value], name = request.form[Consts.NAME.value],
                          email = request.form[Consts.EMAIL.value], type = request.form[Consts.TYPE.value], birth = request.form[Consts.BIRTH.value],
                          sex = request.form[Consts.SEX.value], access = request.form[Consts.ACCESS.value]), ensure_ascii = False)
    except:
        return json.dumps({'error' : Consts.DB_ERROR.value}, ensure_ascii = False)

@app.route('/search_bar', methods = ['POST', 'GET'])
def search_bar():
    return json.dumps(db.search_bar(search = request.form[Consts.SEARCH.value], id = request.form[Consts.ID.value], session = request.form[Consts.SESSION.value]), ensure_ascii = False)

@app.route('/cosmetic_info', methods = ['POST', 'GET'])
def get_cosmetic_info():
    return json.dumps(db.get_cosmetic_info(search = request.form[Consts.SEARCH.value], id = request.form[Consts.ID.value], session = request.form[Consts.SESSION.value]), ensure_ascii = False)

def start_test_server():
    app.run(debug = True)
