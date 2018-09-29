from flask import Flask

app = Flask(__name__)

@app.route('/')
def test():
    return 'hello'

def start_test_server():
    app.run(debug = True)
