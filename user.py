import hashlib

class User:

    def __init__(self, username):
        self.username = username
        md5 = hashlib.md5()
        md5.update(self.username.encode('utf-8'))
        digest = md5.hexdigest()
        self.id = str(int(digest, 16))[0:5]

    def __str__(self):
        return '\n[Username: {}, ID: {}]'.format(self.username, self.id)

    def __eq__(self, other):
        if other == None:
            return False
        elif other.id != self.id:
            return False
        elif other.username != self.username:
            return False
        return True

    def __hash__(self):
        return id
