import pymysql
from singleton import singleton
from getpass import getpass


class sql:
    @staticmethod
    def sql_signIn(kwargs):
        return f"""INSERT INTO user (id, password, name, email, type, birth,
                   sex, access) VALUES ('{kwargs['id']}', '{kwargs['password']}', '{kwargs['name']}','{kwargs['email']}',
                   '{kwargs['type']}', '{kwargs['birth']}', '{kwargs['sex']}', '{kwargs['access']}')"""

    @staticmethod
    def sql_idcheck(kwargs):
        return f"""SELECT EXISTS(SELECT id FROM user WHERE id = '{kwargs['id']}')"""

    @staticmethod
    def sql_login(kwargs):
        return f"""SELECT id, password FROM user WHERE id = '{kwargs['id']}'"""

    @staticmethod
    def sql_cosmetic_search(kwargs):
        return f"""SELECT info.*, ingr.* FROM cinfo info, cingr ingr WHERE
                   info.cname = '{kwargs['cname']}'"""

    @staticmethod
    def sql_search(kwargs):
        return [f"""SELECT cname FROM cinfo WHERE cname
                   LIKE '%{kwargs['name']}%'""",f"""SELECT bname FROM
                   company WHERE bname LIKE '%{kwargs['name']}%'"""]

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

    @staticmethod
    def search_parse(kwargs):
        keys = kwargs.keys()
        if 'cname' in keys:
            return 0
        elif 'company' in keys:
            return 1

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

    def login(self, **kwargs):
        if self.idCheck(id = kwargs['id']) == '1':
            return '2' # sql오류 아이디를 확인하세요
        user = self.s_execute(super().sql_login(kwargs))

        if kwargs['password'] == user[0][1]:
            return '1' #로그인 성공
        else:
            return '0' #로그인 실패

    def cosmetic_search(self, **kwargs):
        info = self.s_execute(super().sql_cosmetic_search(kwargs))
        ingr = []
        for i in info:
            ingr.append(i[4])
        info = {'cname' : info[0][0], 'category' : info[0][1], 'company' : info[0][2], 'ingr' : ingr}
        return info

    def title_search(self, **kwargs): #여기서는 post 매게변수 name으로 받아야 함
        for i in super().sql_search(kwargs):
            print(self.s_execute(i))

db = maria.instance()

db.title_search(name = '화')
