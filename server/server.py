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
        return {'result' : 1}
    else:
        return {'result' : 0}

@app.route('/login', methods = ['POST', 'GET']) # id, password
def login():
    data = request.args.to_dict()
    try:
        print(json.dumps(db.login(data), ensure_ascii = False))
        return json.dumps(db.login(data), ensure_ascii = False)
    except Exception as e:
        print(e)
        return json.dumps({'error' : Consts.DB_ERROR.value}, ensure_ascii = False)

@app.route('/signin', methods = ['POST', 'GET'])
def signIn():
    data = request.args.to_dict()
    try:
        return json.dumps(db.signIn(data), ensure_ascii = False)
    except:
        return json.dumps({'error' : Consts.DB_ERROR.value}, ensure_ascii = False)

@app.route('/search_bar', methods = ['POST', 'GET'])
def search_bar():
    data = request.args.to_dict()
    print(data)
    try:
        print(db.search_bar(data))
        return json.dumps(db.search_bar(data), ensure_ascii = False)
    except:
        return json.dumps({'error' : Consts.DB_ERROR.value})

@app.route('/cosmetic_info', methods = ['POST', 'GET'])
def get_cosmetic_info():
    data = request.form.to_dict()
    try:
        return json.dumps(db.get_cosmetic_info(data), ensure_ascii = False)
    except:
        return json.dumps({'error' : Consts.DB_ERROR.value}, ensure_ascii = False)

@app.route('/get_simple', methods = ['POST', 'GET'])
def get_simple_review():
    data = request.form.to_dict()
    try:
        return json.dumps(db.get_simple_review(data), ensure_ascii = False)
    except:
        return json.dumps({'error' : Consts.DB_ERROR.value}, ensure_ascii = False)

@app.route('/get_detailed', methods = ['POST', 'GET'])
def get_detailed_review():
    data = request.form.to_dict()
    try:
        return json.dumps(db.get_detailed_review(data), ensure_ascii = False)
    except:
        return json.dumps({'error' : Consts.DB_ERROR.value}, ensure_ascii = False)

@app.route('/get_user', methods = ['POST', 'GET'])
def get_user_info():
    data = request.form.to_dict()
    try:
        return json.dumps(db.get_user_info(data), ensure_ascii = False)
    except:
        return json.dumps({'error' : Consts.DB_ERROR.value}, ensure_ascii = False)

@app.route('/get_follow', methods = ['POST', 'GET'])
def get_follow_info():
    data = request.form.to_dict()
    try:
        return json.dumps(db.get_follow_info(data), ensure_ascii = False)
    except:
        return json.dumps({'error' : Consts.DB_ERROR.value}, ensure_ascii = False)

@app.route('/put_detailed')
def put_detailed_review():
    data = request.form.to_dict()
    try:
        if db.put_simple_review(data) == '0':
            return json.dumps({'error' : 'Duplicated entry'})
        return json.dumps({'lcode' : db.get_lcode()})
    except Exception as e:
        return json.dumps({'error' : Consts.DB_ERROR.value}, ensure_ascii = False)

@app.route('/put_simple', methods = ['POST','GET'])
def put_simple_review():
    data = request.form.to_dict()
    try:
        if db.put_simple_review(data) == '0':
            return json.dumps({'error' : 'Duplicated entry'})
        return json.dumps({'lcode' : db.get_lcode()})
    except Exception as e:
        return json.dumps({'error' : Consts.DB_ERROR.value}, ensure_ascii = False)

@app.route('/put_like', methods = ['POST', 'GET'])
def put_like():
    data = request.form.to_dict()
    try:
        if db.put_like(data) == '0':
            return json.dumps({'error' : 'Duplicated entry'})
        return json.dumps({'result' : '1'})
    except:
        return json.dumps({'error' : Consts.DB_ERROR.value}, ensure_ascii = False)

@app.route('/main')
def hello():
    return '김영우 바보'

def start_test_server():
    app.run('0.0.0.0',debug = True)
