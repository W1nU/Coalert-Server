from flask import Flask, request, redirect, jsonify
from database.maria import Maria
from database.sessiondb import Sessiondb
from consts import Consts
from logger import Logger
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

@app.route('/signin', methods = Consts.POST.value)
def signIn():
    try:
        db.signIn(id = request.form[Consts.ID.value], password = request.form[Consts.PASSWORD.value], name = request.form[Consts.NAME.value],
                  email = request.form[Consts.EMAIL.value], type = request.form[Consts.TYPE.value], birth = request.form[Consts.BIRTH.value],
                  sex = request.form[Consts.SEX.value], access = request.form[Consts.ACCESS.value])
        return json.dumps({Consts.ID.value : request.form[Consts.ID.value]})
    except:
        return json.dumps({'error' : '현제 데이터베이스 서버에 접속이 불안정합니다\n잠시후 다시 시도해 주세요!'})

def login_session(id):
    if sessiondb.isExist_session(id) == 1:
        sessiondb.drop_session(id)
    return sessiondb.create_session(id)

def always_variable(info):
    return info.form[Consts.ID.value], info.form[Consts.SESSION.value]

def start_test_server():
    app.run(debug = True)
