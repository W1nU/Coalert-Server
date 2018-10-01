import pymysql
from .singleton import Singleton
from getpass import getpass
from consts import Consts

class sql:
    @staticmethod
    def sql_signIn(kwargs):
        return f"""INSERT INTO user (id, password, name, email, type, birth,
                   sex, access) VALUES ('{kwargs[Consts.ID.value]}', '{kwargs[Consts.PASSWORD.value]}',
                   '{kwargs[Consts.NAME.value]}','{kwargs[Consts.EMAIL.value]}','{kwargs[Consts.TYPE.value]}',
                   '{kwargs[Consts.BIRTH.value]}', '{kwargs[Consts.SEX.value]}', '{kwargs[Consts.ACCESS.value]}')"""

    @staticmethod
    def sql_idcheck(kwargs):
        return f"""SELECT EXISTS(SELECT id FROM user WHERE id = '{kwargs[Consts.ID.value]}')"""

    @staticmethod
    def sql_login(kwargs):
        return f"""SELECT id, password FROM user WHERE id = '{kwargs[Consts.ID.value]}'"""

    @staticmethod
    def sql_cosmetic_search(kwargs):
        return f"""SELECT info.*, ingr.* FROM cinfo info, cingr ingr WHERE
                   info.cname = '{kwargs[Consts.CNAME.value]}'"""

    @staticmethod
    def sql_search(kwargs):
        return [f"""SELECT cname FROM cinfo WHERE cname
                   LIKE '%{kwargs[Consts.CNAME.value]}%'""",f"""SELECT bname FROM
                   company WHERE bname LIKE '%{kwargs[Consts.CNAME.value]}%'"""] # 사람 검색 기능 추가해야함

    @staticmethod
    def sql_insertSimpleReview(kwargs):
        return f"""INSERT INTO simple_review (id, cname, oneline, rate) VALUES
                   ({kwargs[enumulate.ID.value]}, {kwargs[enumerate.CNAME.value]},
                   {kwargs[enumulate.ONELINE.value], {kwargs[enumerate.RATE.value]}})"""

    @staticmethod
    def sql_getUserInfo(kwargs):
        return f"""SELECT name, email, type, birth, sex, access name FROM user
                    WHERE id = '{kwargs[Consts.ID.value]}'"""

    @staticmethod
    def sql_getUserSimpleReview(kwargs):
        if Consts.ID.value in kwargs.keys():
            return f"""SELECT * FROM simple_review WHERE id = '{kwargs[Consts.ID.value]}'"""
        elif Consts.CNAME.value in kwargs.keys():
            return f"""SELECT * FROM simple_review WHERE cname = '{kwargs[Consts.CNAME.value]}'"""

    @staticmethod
    def sql_getUserDetailedReview(kwargs):
        if Consts.ID.value in kwargs.keys():
            return f"""SELECT * FROM detailed_review WHERE id = '{kwargs[Consts.ID.value]}'"""
        elif Consts.CNAME.value in kwargs.keys():
            return f"""SELECT * FROM detailed_review WHERE cname = '{kwargs[Consts.CNAME.value]}'"""

class Maria(sql, Singleton):
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
        if self.idCheck(id = kwargs[Consts.ID.value]) == '1':
            return '2' # sql오류 아이디를 확인하세요
        user = self.s_execute(super().sql_login(kwargs))

        if kwargs[Consts.PASSWORD.value] == user[0][1]:
            return '1' #로그인 성공
        else:
            return '0' #로그인 실패

    def cosmetic_search(self, **kwargs):
        info = self.s_execute(super().sql_cosmetic_search(kwargs))
        ingr = []
        for i in info:
            ingr.append(i[4])
        info = {Consts.CNAME.value : info[0][0], Consts.CATEGORY.value : info[0][1], Consts.COMPANY.value : info[0][2], Consts.INGR.value : ingr}
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
        result = {Consts.CNAME.value : result[0], Consts.COMPANY.value : result[1]}
        return result

    def get_user_info(self, **kwargs):
        info = self.s_execute(super().sql_getUserInfo(kwargs))[0]
        result = {Consts.NAME.value : info[0], Consts.EMAIL.value : info[1], Consts.TYPE.value : info[2],
                  Consts.BIRTH.value : info[3], Consts.SEX.value : info[4], Consts.ACCESS.value : info[5]}
        return result

    def get_user_simple_review(self, **kwargs):
        result = []
        info = self.s_execute(super().sql_getUserSimpleReview(kwargs))
        for i in info:
            result.append({Consts.ID.value : i[1], Consts.CNAME.value : i[2], Consts.CONTENT.value : i[3], Consts.RATE.value : i[4]})
        return result

    def get_detailed_review(self, **kwargs):
        result = []
        info = self.s_execute(super().sql_getUserDetailedReview(kwargs))
        print(info)
