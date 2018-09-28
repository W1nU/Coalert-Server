import pymysql
from singleton import singleton
from getpass import getpass

class __sql:
    @staticmethod
    def __signIn(kwargs):
        print( f'''INSERT INTO user (id, password, name, type, birth,
                   sex, access) VALUES (kwargs[id], kwargs[password], kwargs[name],
                   kwargs[type], kwargs[bitrh], kwargs[sex], kwargs[access])''')

class maria(singleton, __sql):
    def __init__(self):
        user = input('Insert username : ')
        password = getpass('Insert password : ')

        self.connect = pymysql.connect(host = 'localhost',
                                  port = 3306,
                                  user = user,
                                  password = password,
                                  db = 'coalert',
                                  charset = 'utf8',
                                  unix_socket = '/Applications/mampstack-7.0.30-0/mysql/tmp/mysql.sock')
        self.cursor = self.connect.cursor()

    def execute(self, sql):
        self.cursor.execute(sql)
        self.connect.commit()

    def signIn(self, **kwargs):
        __signIn(kwargs)

    def test(self):
        print('hello')



db = maria.instance()
db.signIn({'id' : 'hello', 'password' : 'password', 'name' : 'name', 'type' : 1, 'birth' : '2018-01-01', 'sex' : 1, 'access' : 1})
