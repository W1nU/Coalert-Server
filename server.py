from flask import Flask, request, redirect, jsonify
from database.maria import Maria
from database.sessiondb import Sessiondb
from consts import Consts
import json

app = Flask(__name__)
db = Maria.instance()
sessiondb = Sessiondb.instance()

@app.route('/test', methods = Consts.POST.value)
def test():
    id = request.form[Consts.ID.value]
    return sessiondb.open_session(id)

@app.route('/login', methods = Consts.POST.value) # id, password
def login():
    id = request.form[Consts.ID.value]
    password = request.form[Consts.PASSWORD.value]
    status = db.login(id = id, password = password)
    if status == '1':
        session_key = self.login_session(id)
        return json.dumps({Consts.ID.value : id, Consts.SESSION.value : session_key}, ensure_ascii = False)
    elif status == '2':
        return json.dumps({'error' : '아이디를 확인하세요!'}, ensure_ascii = False)
    else:
        return json.dumps({'error' : '아이디와 비밀번호를 확인하세요!'}, ensure_ascii = False)

def login_session(id):
    if sessiondb.isExist_session(id) == 1:
        sessiondb.drop_session(id)
    return sessiondb.create_session(id)

def start_test_server():
    app.run(debug = True)
