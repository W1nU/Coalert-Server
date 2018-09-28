import pymysql
from singleton import singleton
from getpass import getpass
import json

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
                   company WHERE bname LIKE '%{kwargs['name']}%'"""] # 사람 검색 기능 추가해야함

    @staticmethod
    def sql_userInfo(kwargs):
        return f"""SELECT name, email, type, birth, sex, access name FROM user
                    WHERE id = '{kwargs['id']}'"""

    @staticmethod
    def sql_userSimpleReview(kwargs):
        if 'id' in kwargs.keys():
            return f"""SELECT * FROM simple_review WHERE id = '{kwargs['id']}'"""
        elif 'cname' in kwargs.keys():
            return f"""SELECT * FROM simple_review WHERE cname = '{kwargs['cname']}'"""

    @staticmethod
    def sql_userDetailedReview(kwargs):
        if 'id' in kwargs.keys():
            return f"""SELECT * FROM detailed_review WHERE id = '{kwargs['id']}'"""
        elif 'cname' in kwargs.keys():
            return f"""SELECT * FROM detailed_review WHERE cname = '{kwargs['cname']}'"""

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
        result = [[],[]]
        sql_list = super().sql_search(kwargs)
        info = [self.s_execute(sql_list[i]) for i in range(0,2)]
        for i in range(0,2):
            if info[i] == ():
                continue
            else:
                for j in info[i]:
                    if i == 0:
                        result[0].append(j[0])
                    else:
                        result[1].append(j[0])
        result = {'cname' : result[0], 'company' : result[1]}
        return result

    def get_user_info(self, **kwargs):
        info = self.s_execute(super().sql_userInfo(kwargs))[0]
        result = {'name' : info[0], 'email' : info[1], 'type' : info[2],
                  'bitrh' : info[3], 'sex' : info[4], 'access' : info[5]}
        return result

    def get_user_simple_review(self, **kwargs):
        result = []
        info = self.s_execute(super().sql_userSimpleReview(kwargs))
        for i in info:
            result.append({'author' : i[1], 'cname' : i[2], 'content' : i[3], 'rate' : i[4]})
        return result

    def get_detailed_review(self, **kwargs):
        result = []
        info = self.s_execute(super().sql_userDetailedReview(kwargs))
        print(info)


db = maria.instance()
