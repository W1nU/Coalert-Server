import pymysql
from singleton import singleton
from getpass import getpass

class sql:
    @staticmethod
    def sql_signIn(kwargs):
        return f"""INSERT INTO user (id, password, name, type, birth,
                   sex, access) VALUES ('{kwargs['id']}', '{kwargs['password']}', '{kwargs['name']}',
                   '{kwargs['type']}', '{kwargs['birth']}', '{kwargs['sex']}', '{kwargs['access']}')"""

    @staticmethod
    def sql_idcheck(kwargs):
        return f"""SELECT EXISTS(SELECT id FROM user WHERE id = '{kwargs['id']}')"""

class maria(sql, singleton):
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

    def s_execute(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def signIn(self, **kwargs):
        self.execute(super().sql_signIn(kwargs))
        return '1'
        
    def idCheck(self, **kwargs):
        if self.s_execute(self.sql_idcheck(kwargs))[0][0] == 1:
            return '0' #불가능
        else:
            return '1' #가능

db = maria.instance()
