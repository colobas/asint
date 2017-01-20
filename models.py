from google.appengine.ext import ndb
import hashlib

def encodeName(name):
    sha1 = hashlib.sha1()
    sha1.update(name.encode('utf-8'))
    return int(sha1.hexdigest()[0:5], 16)

class User(ndb.Model):
    username = ndb.StringProperty()
    id = ndb.ComputedProperty(lambda self: encodeName(self.username))

class Ticket(ndb.Model):
    room = ndb.KeyProperty(kind="Room")
    user = ndb.KeyProperty(kind="User")

class Room(ndb.Model):
    name = ndb.StringProperty()
    id = ndb.IntegerProperty()
    campus = ndb.StringProperty()
    capacity = ndb.IntegerProperty()
    occupancy = ndb.IntegerProperty()
