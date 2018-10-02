from flask import Flask, request, redirect, jsonify
from database.manager import dbManager
from consts import Consts
from log.logger import Logger
import json

app = Flask(__name__)
db = dbManager.instance()

@app.route('/test', methods = Consts.POST.value)
def test():
    id = request.form[Consts.ID.value]
    return sessiondb.open_session(id)

@app.route('/login', methods = Consts.POST.value) # id, password
def login():
    id = request.form[Consts.ID.value]
    password = request.form[Consts.PASSWORD.value]
    return json.dumps(db.login(id = id, password = password), ensure_ascii = False)
    return json.dumps({'error' : '현제 데이터베이스 서버에 접속이 원할하지 않습니다.\n잠시후 다시 시도해 주세요!'}, ensure_ascii = False)

@app.route('/signin', methods = Consts.POST.value)
def signIn():
    try:
        db.signIn(id = request.form[Consts.ID.value], password = request.form[Consts.PASSWORD.value], name = request.form[Consts.NAME.value],
                  email = request.form[Consts.EMAIL.value], type = request.form[Consts.TYPE.value], birth = request.form[Consts.BIRTH.value],
                  sex = request.form[Consts.SEX.value], access = request.form[Consts.ACCESS.value])
        return json.dumps({Consts.ID.value : request.form[Consts.ID.value]})
    except:
        return json.dumps({'error' : '현제 데이터베이스 서버에 접속이 불안정합니다\n잠시후 다시 시도해 주세요!'})

def always_variable(info):
    return info.form[Consts.ID.value], info.form[Consts.SESSION.value]

def start_test_server():
    app.run(debug = True)
