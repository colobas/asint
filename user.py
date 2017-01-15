import hashlib

class User:

    def __init__(self, username):
        self.username = username
        sha1 = hashlib.sha1()
        sha1.update(self.username.encode('utf-8'))
        digest = sha1.hexdigest()[0:5]
        self.id = int(digest, 16)

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
        return self.id
