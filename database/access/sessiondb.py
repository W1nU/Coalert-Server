from redis import Redis
from uuid import uuid4
from singleton import Singleton
from time import time

class Redisdb(Singleton):
    ip = 'localhost'
    port = 6379
    timeout = 3600

    def __init__(self):
        self.connect = Redis(self.ip, self.port)

    def is_exist_session(self, id):
        return self.connect.exists(id)

    def reset_timeout(self, id):
        if self.is_exist_session(id) == 1:
            self.connect.expire(id, self.timeout)
            return '1'
        else:
            return '0'

    def drop_session(self, id):
        if self.is_exist_session(id) == 1:
            self.connect.delete(id)
            return '1'
        else:
            return '0'

    def create_session(self, id):
        if self.is_exist_session(id) == 1:
            self.drop_session(id)
        time_now = str(time())
        session_key  = str(uuid4())+time_now
        self.connect.setex(id, session_key, self.timeout)
        return session_key

    def id_block(self, id):
        self.connect.setex(id, 'id blocked for a while', 300)

    def open_session(self, id):
        if self.is_exist_session(id) == 0:
            return '0'
        else:
            self.reset_timeout(id)
            return self.connect.get(id).decode('utf-8') # 세션이 있으면 세션키 리턴
