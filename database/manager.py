from .access.maria import Maria
from .access.sessiondb import Sessiondb
from .access.mongo import Mongo
from consts import Consts
from singleton import Singleton

class dbManager(Singleton):
    def __init__(self):
        self.maria = Maria.instance()
        self.mongo = Mongo.instance()
        self.redis = Sessiondb.instance()

    def idChesk(self):
        if self.maria.idCheck() == 0:
            return '1'
        else:
            return '0'

    def login(self, **kwargs):
        password = self.maria.get_Password(kwargs)[0][0]
        print(password)
        if password == kwargs[Consts.PASSWORD.value]:
            session_key = self.redis.create_session(kwargs[Consts.ID.value])
            return {Consts.ID.value : kwargs[Consts.ID.value], Consts.SESSION.value : session_key}
        elif password == ():
            return {'error' : '존재하지 않는 아이디입니다!'}
        else:
            return {'error' : '아이디와 비밀번호를 확인하세요!'}
