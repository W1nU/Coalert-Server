from redis import Redis
from uuid import uuid4
from singleton import Singleton
from time import time

class Sessiondb(Singleton):
    ip = localhost
    port = 6379
    timeout = 3600

    def __init__(self):
        self.connect = Redis(self.ip, self.port)

    def isExist_session(self, id):
        return self.commit.exists(id)

    def create_session(self, id):
        if self.isExist_session(id) == 1:
            return '0' # 이미 세션 존재
        time = str(time())
        session_key  = str(uuid4())+time
        self.connect.setex(id, session_key, self.timeout)
        return session_key

    def open_session(self, id):
        if isExist_session(id) == 0:
            return '0' # 세션이 없으면 만들고 세션키 리턴
        else:
            return self.connect.get(id) # 세션이 있으면 세션키 리턴
