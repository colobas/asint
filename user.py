import hashlib

class User:

    def __init__(self, username):
        self.username = username
        self.id = id(self)

    def __str__(self):
        return '\n[Username: {}, ID: {}]'.format(self.username, self.id)

    def getId(self):
        return self.id

    def getUsername(self):
        return  self.username