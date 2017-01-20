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


# Index, o que aparece no browser quando se acede ao servidor
@app.route('/')
def home():
    return template(hometemplate)


# Funcoes admin <--> fenix


@app.route('/campus')
def listCampus():
    r = urlfetch.fetch("http://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces")
    response = json.loads(r.content)
    output = "[" 

    for campus in response:
        output += "{\""+campus["name"]+"\","+campus["id"]+"},"
    return output[:-1] + "]"


def listContainedSpaces(space_id):
    """
    return list of tuples, one per contained space: (name, id)
    """
    r = urlfetch.fetch("http://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/"+space_id)
    response = json.loads(r.content)
    output = "[ "

    for contained in response["containedSpaces"]:
        output += "{\""+contained["name"]+"\","+contained["id"]+"},"
    return output[:-1] + "]"

@app.route('/campus/<campus_id>')
def listCampusBuildings(campus_id):
    return listContainedSpaces(campus_id)


@app.route('/building/<building_id>')
def listBuildingFloors(building_id):
    return listContainedSpaces(building_id)

@app.route('/floor/<floor_id>')
def listFloorRooms(floor_id):
    return listContainedSpaces(floor_id)

def getFenixRoom(room_id):
    r = urlfetch.fetch("http://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/" + room_id)
    return json.loads(r.content)


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

@app.route('/user/<userid>')
def user(userid):
    _userid = int(userid)

    user = getUserByID(_userid)
    if user != None:
        return userLoggedInTemplate(user)
    else:
        return "no such user"


@app.get('/listrooms')
def listrooms():

    qry = Room.query()
    response = "["

    for room in qry:
        response += """
            {{
                "name":"{}",
                "building":"{}",
                "campus":"{}",
                "occupancy":{},
                "capacity":{},
                "id":"{}"
            }},
        """.format(room.name, room.building, room.campus, room.occupancy, room.capacity, room.id)

    response = response[:-10]+ "]"
    return response


def getUserByID(id):
    qry = User.query(User.id == id)
    return qry.get()

def getRoomByID(id):
    qry = Room.query(Room.id == id)
    return qry.get()


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

    _users = "[ "

    checkedin = False

    tickets = Ticket.query()

    for ticket in tickets:
        if ticket.room == room:
            _users += '{{"username":"{}"}},'.format(ticket.user.username)
            if _userid != 0:
                if ticket.user == user:
                    checkedin = True

    _users = _users[:-1] + "]"

    return """
            {{
                "name":"{}",
                "campus":"{}",
                "occupancy":{},
                "capacity":{},
                "users":{},
                "checkedin":{}
            }}
        """.format(room.name, room.campus, room.occupancy, room.capacity, _users, "true" if checkedin else "false")


@app.get('/checkin/<roomid>/<userid>')
def checkin(roomid, userid):
    _userid = int(userid)
    _roomid = int(roomid)

    room = getRoomByID(_roomid)
    user = getUserByID(_userid)

    if room != None and user != None:
        if room.occupancy + 1 <= room.capacity:
            tk = Ticket(room=room, user=user)
            tk.put()
            room.occupancy += 1

    return ""

@app.get('/checkout/<userid>')
def checkout(userid):
    _userid = int(userid)
    user = getUserByID(_userid)

    if userid != None:
        qry = Ticket.query(user=user)
        res = qry.get()
        if res != None:
            res.room.occupancy -= 1
            res.key.delete()

    return ""


@app.route('/admin')
def admin():
    return adminLoggedInTemplate("")

@app.route('/admin/addroom/<roomid>')
def addRoom(roomid):
    if getRoomByID(int(roomid)) != None:
        return roomview(int(roomid),0)
    try:
        _room = getFenixRoom(roomid)
        room = Room(name=_room["name"], id=int(_room["id"]), 
                    capacity=int(_room["capacity"]["normal"]), 
                    occupancy=0)
        room.put()
        return roomview(_room["id"],0)
    except:
        return "failed to add room."

def userLoggedInTemplate(user):
    return template(usertemplate, user=user)


def adminLoggedInTemplate(adminscript):
    return template(admintemplate, username=adminscript)


if __name__ == '__main__':
    run(app, host='localhost', port=8080)
