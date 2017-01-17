import time

class Ticket:

    def __init__ (self, room_id, username):
        self.room_id=room_id
        self.time=time.time()
        self.username=username

