import time

class Ticket:

    def __init__ (self, roomid, user):
        self.roomid=roomid
        self.time=time.time()
        self.user=user.id

