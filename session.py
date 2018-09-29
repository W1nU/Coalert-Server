import uuid
import hashlib

class Session:
    def __init__(self):
        self.key = uuid.uuid4()
        print(self.key)
