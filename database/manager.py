from .access.maria import Maria
from .access.sessiondb import Redisdb
from .access.mongo import Mongo
from consts import Consts
from singleton import Singleton

class dbManager(Singleton):
    def __init__(self):
        self.maria = Maria.instance()
        self.mongo = Mongo.instance()
        self.redis = Redisdb.instance()

    def id_block(self, kwargs):
        #This block works for prevention id duplicated insert,
        #In signIn, it will block id 5mins after idCheck method called
        self.redis.id_block(kwargs[Consts.ID.value])

    def id_check(self, kwargs):
        if self.maria.id_check(kwargs)[0][0] == 0 and self.Redisdb.open_session(kwargs[Consts.ID.value]) != '0':
            self.Redisdb.id_block(kwargs[Consts.ID.value])
            return '1'
        else:
            return '0'

    def email_check(self, kwargs):
        if self.maria.email_check(kwargs)[0][0] == 0:
            return '1'
        else:
            return '0'

    def session_check(self, func, *args):
        if args[0][Consts.SESSION.value] == self.redis.open_session(args[0][Consts.ID.value]):
            return func(args[0])
        else:
            return '0'

    def login(self, kwargs):
        password = self.maria.get_password(kwargs)
        if password == ():
            return {'error' : '존재하지 않는 아이디입니다!'}
        elif password[0][0] == kwargs[Consts.PASSWORD.value]:
            session_key = self.redis.create_session(kwargs[Consts.ID.value])
            return {Consts.ID.value : kwargs[Consts.ID.value], Consts.SESSION.value : session_key}
        else:
            return {'error' : '아이디와 비밀번호를 확인하세요!'}

    def sign_in(self, kwargs):
        if self.id_check(kwargs) == '0' or self.Redisdb.open_session(kwargs[Consts.ID.value]) != '0':
            return {'error' : '이미 존재하는 ID입니다!'}
        elif self.email_check(kwargs) == '0':
            return {'error' : '이미 존재하는 Email입니다!'}
        else:
            self.maria.signIn(kwargs)
            return {Consts.ID.value : kwargs[Consts.ID.value]}

    def search_bar(self, kwargs):
        try:
            return self.session_check(self.maria.search_bar, kwargs)
        except:
            return {'error' : 're-login'}

    def get_simple_review(self, kwargs):
        try:
            return self.session_check(self.maria.get_simple_review, kwargs)
        except:
            return {'error' : 're-login'}

    def get_cosmetic_info(self, kwargs):
        try:
            return self.session_check(self.maria.get_cosmetic_info, kwargs)
        except:
            return {'error' : 're-login'}

    def get_user_info(self, kwargs):
        try:
            return self.session_check(self.maria.get_user_info, kwargs)
        except:
            return {'error' : 're-login'}
