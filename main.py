# coding=utf-8

"""
O browser fala com o servidor através de pedidos HTTP. Para tal utiliza-se JavaScript.
O JS serve para a página não ter de ser actualizada sempre que se faz algum pedido.
Cada vez que se faz um pedido, o browser envia-o por HTTP ao servidor, que responde com o resultado do pedido.
Quando um pedido é enviado ao servidor, ele recebe-o, processa-o e retorna o resultado.
Consoante a resposta recebida pelo browser, este corre uma tarefa/função específica (JS).

"""
from google.appengine.ext import ndb
from google.appengine.api import urlfetch
from bottle import Bottle, run, template, request
import json
from models import User, Room, Ticket

app = Bottle()

usertemplate = ""
hometemplate = ""
admintemplate = ""

with open("user_template.st", "r") as f:
    usertemplate = f.read()

with open("admin_template.st", "r") as f:
    admintemplate = f.read()

with open("home.st", "r") as f:
    hometemplate = f.read()


def getUserByID(id):
    qry = User.query(User.id == id)
    return qry.get()

def getRoomByID(id):
    qry = Room.query(Room.id == id)
    return qry.get()


def listContainedSpaces(space_id, looking_for):
    r = urlfetch.fetch("http://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/"+space_id)
    response = json.loads(r.content)
    output = "[ "

    for contained in response["containedSpaces"]:
        if contained["type"] == looking_for:
            output += "{\"name\":\""+contained["name"].encode('utf-8')+"\",\"id\":"+str(contained["id"])+"},"
        else:
            _nested = listContainedSpaces(str(contained["id"]), looking_for)
            nested = json.loads(_nested)
            for nested_cont in nested:
                output += "{\"name\":\""+nested_cont["name"].encode('utf-8')+"\",\"id\":"+str(nested_cont["id"])+"},"

    return output[:-1] + "]"

def getFenixRoom(room_id):
    r = urlfetch.fetch("http://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/" + room_id)
    return json.loads(r.content)


def userLoggedInTemplate(user):
    return template(usertemplate, user=user)


def adminLoggedInTemplate(adminscript):
    return template(admintemplate, username=adminscript)


def viewroom(room, user, _userid, tk=None):

    _users = "[ "

    checkedin = False
    tickets = Ticket.query().fetch()

    for ticket in tickets:
        if ticket.room == room.key:
            _users += '{{"username":"{}"}},'.format(ticket.user.get().username)
            if _userid != 0 and tk == None:
                if ticket.user == user.key:
                    checkedin = True

    # this has to be done, because when checking in, the query sometimes doesn't
    # retrieve the last ticket (the one added when checking in).
    if tk != None:
        checkedin = True
        if user.username not in _users:
            _users += '{{"username":"{}"}},'.format(user.username)


    return """
            {{
                "name":"{}",
                "campus":"{}",
                "occupancy":{},
                "capacity":{},
                "users":{},
                "checkedin":{}
            }}
        """.format(room.name, room.campus, room.occupancy, room.capacity, _users[:-1]+"]", "true" if checkedin else "false")


@app.get('/')
def home():
    return template(hometemplate)


@app.post('/')
def login():
    # Dados enviados pelo browser
    # Divididos em username e mode (reg ou log)

    data = request.forms.get('data').split(",")
    username = data[0]
    mode = data[1]

    # Se o user for admin, retorna com id 0
    if username == "admin":
        return "0"

    # REG - Caso existam users registados, se o nome introduzido já existir, impossível registar
    # LOG - Se o nome introduzido já estiver registado, devolve username e id.
    qry = User.query(User.username == username)
    res = qry.get()


    if res != None:
        if mode == "log":
            return str(res.id)
        else:
            return "-1"
    else:
        if mode == "reg":
            new_user = User(username=username)
            new_user.put()
            return str(new_user.id)
        else:
            return "-1"


@app.get('/admin')
def admin():
    return adminLoggedInTemplate("")


@app.get('/admin/campi')
def listCampus():
    r = urlfetch.fetch("http://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces")
    response = json.loads(r.content)
    output = "[ "

    for contained in response:
        output += "{\"name\":\""+contained["name"]+"\",\"id\":"+contained["id"]+"},"
    return output[:-1] + "]"


@app.get('/admin/campus/<campus_id>')
def listCampusBuildings(campus_id):
    return listContainedSpaces(campus_id, "BUILDING")


@app.get('/admin/building/<building_id>')
def listBuildingFloors(building_id):
    return listContainedSpaces(building_id, "FLOOR")


@app.get('/admin/floor/<floor_id>')
def listFloorRooms(floor_id):
    return listContainedSpaces(floor_id, "ROOM")


@app.get('/admin/addroom/<roomid>')
def addRoom(roomid):
    if getRoomByID(int(roomid)) != None:
        return roomview(roomid, 0)
    try:
        _room = getFenixRoom(roomid)
        if (_room["capacity"]["normal"]) == 0:
            return "-2"

        room = Room(name=_room["name"].encode('utf-8'), id=int(_room["id"]),
                    capacity=int(_room["capacity"]["normal"]),
                    campus=_room["topLevelSpace"]["name"].encode('utf-8'),
                    occupancy=0)
        room.put()
        return roomview(roomid, 0)
    except:
        return "-1"


@app.get('/user/<userid>')
def user(userid):
    _userid = int(userid)

    user = getUserByID(_userid)
    if user != None:
        return userLoggedInTemplate(user)
    else:
        return "no such user"


@app.get('/listrooms')
def listrooms():
    qry = Room.query().fetch()
    response = "["

    for room in qry:
        response += """
            {{
                "name":"{}",
                "campus":"{}",
                "occupancy":{},
                "capacity":{},
                "id":"{}"
            }},
        """.format(room.name, room.campus, room.occupancy, room.capacity, room.id)

    response = response[:-10] + "]"
    return response


@app.get('/room/<roomid>/<userid>')
def roomview(roomid, userid):
    _roomid = int(roomid)
    _userid = int(userid)

    room = getRoomByID(_roomid)
    if room == None:
        return "-1"

    if _userid != 0:
        user = getUserByID(_userid)
        if user == None:
            return "-1"
    else:
        user = None

    return viewroom(room, user, _userid)


@app.get('/checkin/<roomid>/<userid>')
def checkin(roomid, userid):
    checkout(userid)

    _userid = int(userid)
    _roomid = int(roomid)

    room = getRoomByID(_roomid)
    user = getUserByID(_userid)

    if room != None and user != None:
        if room.occupancy + 1 <= room.capacity:
            tk = Ticket(room=room.key, user=user.key)
            tk.put()
            room.occupancy += 1
            room.put()
            return viewroom(room, user, _userid, tk)
    return viewroom(room, user, _userid)


@app.get('/checkout/<userid>')
def checkout(userid):
    _userid = int(userid)
    roomid = 0
    user = getUserByID(_userid)

    if user != None:
        qry = Ticket.query(Ticket.user == user.key)
        res = qry.get()
        if res != None:
            room = res.room.get()
            roomid = room.id
            room.occupancy -= 1
            room.put()
            res.key.delete()

    if roomid != 0:
        return viewroom(room, user, _userid)
    else:
        return "{}"


if __name__ == '__main__':
    run(app, host='localhost', port=8080)
