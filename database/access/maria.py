import pymysql
from singleton import Singleton
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
    def sql_emailCheck(kwargs):
        return f"""SELECT EXISTS(SELECT email FROM user WHERE email = '{kwargs[Consts.EMAIL.value]}')"""

    @staticmethod
    def sql_getPassword(kwargs):
        return f"""SELECT password FROM user WHERE id = '{kwargs[Consts.ID.value]}'"""

    @staticmethod
    def sql_getCosmeticInfo(kwargs):
        return f"""SELECT info.*, ingr.* FROM cinfo info, cingr ingr WHERE
                   info.cname = '{kwargs[Consts.SEARCH.value]}' AND ingr.cname = '{kwargs[Consts.SEARCH.value]}'"""

    @staticmethod
    def sql_searchBar(kwargs):
        return [f"""SELECT cname FROM cinfo WHERE cname
                   LIKE '%{kwargs[Consts.SEARCH.value]}%'""",f"""SELECT bname FROM
                   company WHERE bname LIKE '%{kwargs[Consts.SEARCH.value]}%'""",
                   f"""SELECT name FROM user WHERE name LIKE '%{kwargs[Consts.SEARCH.value]}%'"""]

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
    def sql_getSimpleReview(kwargs):
        if Consts.CNAME.value in kwargs.keys():
            return f"""SELECT * FROM simple_review WHERE cname = '{kwargs[Consts.ID.value]}' LIMIT {kwargs[Consts.START.value]}, {kwargs[Consts.COUNT.value]}"""
        elif Consts.ID.value in kwargs.keys():
            return f"""SELECT * FROM simple_review WHERE id = '{kwargs[Consts.CNAME.value]}' LIMIT {kwargs[Consts.START.value]}, {kwargs[Consts.COUNT.value]}"""

    @staticmethod
    def sql_getDetailedReview(kwargs):
        if Consts.CNAME.value in kwargs.keys():
            return f"""SELECT * FROM detailed_review WHERE cname = '{kwargs[Consts.ID.value]}' LIMIT {kwargs[Consts.START.value]}, {kwargs[Consts.COUNT.value]}"""
        elif Consts.ID.value in kwargs.keys():
            return f"""SELECT * FROM detailed_review WHERE id = '{kwargs[Consts.CNAME.value]}'LIMIT {kwargs[Consts.START.value]}, {kwargs[Consts.COUNT.value]}"""

    @staticmethod
    def sql_getFollowInfo(kwargs):
        return f"""SELECT * FROM follow_list WHERE id = '{kwargs[Consts.SEARCH.value]}' OR fid = '{kwargs[Consts.SEARCH.value]}'"""

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

    def id_check(self, kwargs):
        return self.s_execute(super().sql_idcheck(kwargs))

    def email_check(self, kwargs):
        return self.s_execute(super().sql_emailCheck(kwargs))

    def get_password(self, kwargs):
        return self.s_execute(super().sql_getPassword(kwargs))

    def sign_in(self, kwargs):
        self.execute(super().sql_signIn(kwargs))
        return '1'

    def get_cosmetic_info(self, kwargs):
        info = self.s_execute(super().sql_getCosmeticInfo(kwargs))
        if info == ():
            return {'error' : 'No results, Check your parameter value'}
        else:
            ingr = []
            for i in info:
                ingr.append(i[5])
            info = {Consts.CNAME.value : info[0][1], Consts.CATEGORY.value : info[0][2], Consts.RANK.value : info[0][0], Consts.COMPANY.value : info[0][3], Consts.INGR.value : ingr}
            return info

    def search_bar(self, kwargs): #여기서는 post 매게변수 search으로 받아야 함
        result = [[],[],[]]
        sql_list = super().sql_searchBar(kwargs)
        info = [self.s_execute(sql_list[i]) for i in range(len(sql_list))]
        for i in range(0,3):
            if info[i] == ():
                continue
            else:
                for j in info[i]:
                    if i == 0:
                        result[0].append(j[0])
                    elif i == 1:
                        result[1].append(j[0])
                    else:
                        result[2].append(j[0])
        result = {Consts.CNAME.value : result[0], Consts.COMPANY.value : result[1], Consts.NAME.value : result[2]}
        return result

    def get_user_info(self, kwargs):
        info = self.s_execute(super().sql_getUserInfo(kwargs))[0]
        if info == ():
            return {'error' : 'No results, Check your parameter value'}
        result = {Consts.NAME.value : info[0], Consts.EMAIL.value : info[1], Consts.TYPE.value : info[2],
                  Consts.BIRTH.value : info[3].strftime('%Y-%m-%d'), Consts.SEX.value : info[4], Consts.ACCESS.value : info[5]}
        return result

    def get_simple_review(self, kwargs):
        result = []
        info = self.s_execute(super().sql_getSimpleReview(kwargs))
        if info == ():
            return {'error' : 'No results, Check your parameter value'}
        for i in info:
            result.append({Consts.ID.value : i[1], Consts.CNAME.value : i[2], Consts.ONELINE.value : i[3], Consts.RATE.value : i[4]})
        return result

    def get_detailed_review(self, kwargs):
        result = []
        info = self.s_execute(super().sql_getDetailedReview(kwargs))
        if info == ():
            return {'error' : 'No results, Check your parameter value'}
        return info

    def get_follow_info(self, kwargs):
        info = self.s_execute(super().sql_getFollowInfo(kwargs))
        if info == ():
            return {'error' : 'No results, Check your parameter value'}
        return {i[0]+1 : i[1] for i in enumerate(info)}
