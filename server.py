from flask import Flask, request, redirect, jsonify
from database.maria import Maria
from database.sessiondb import Sessiondb
from consts import Consts
from session import Session


app = Flask(__name__)
db = Maria.instance()

@app.route('/')
def test():
    return 'hello'

@app.route('/login', methods = Consts.POST.value) # id, password
def login():
    status = db.login(id = request.form[Consts.ID.value], password = request.form[Consts.PASSWORD.value])
    if status == '1':
        id = Session()
        return 'logged in'
    elif status == '2':
        return 'Check your Id & Password'
    return status

def start_test_server():
    app.run(debug = True)
