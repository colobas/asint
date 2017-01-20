# coding=utf-8

"""
O browser fala com o servidor através de pedidos HTTP. Para tal utiliza-se JavaScript.
O JS serve para a página não ter de ser actualizada sempre que se faz algum pedido.
Cada vez que se faz um pedido, o browser envia-o por HTTP ao servidor, que responde com o resultado do pedido.
Quando um pedido é enviado ao servidor, ele recebe-o, processa-o e retorna o resultado.
Consoante a resposta recebida pelo browser, este corre uma tarefa/função específica (JS).

"""
from google.appengine.ext import ndb
from bottle import Bottle, run, template, request
import json
import requests
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

def listCampus():
    r = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces")
    response = r.json()
    output = []

    for i in range(0, len(response)):
        output.append(response[i]["name"])
    return output


def getCampusID(name):
    r = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces")
    response = r.json()
    if name == "Alameda":
        return response[0]["id"]
    elif name == "Nuclear":
        return response[1]["id"]
    elif name == "Tagus":
        return response[2]["id"]
    else:
        return "Invalid campus name"


def listBuildings(campus):
    campus_id = getCampusID(campus)
    r = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/"+campus_id)
    response = r.json()
    output = []

    for i in range(0, len(response["containedSpaces"])):
        output.append(response["containedSpaces"][i]["name"])
    return output


def getBuildingID(campus, buildingName):
    campus_id = getCampusID(campus)
    r = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/"+campus_id)
    response = r.json()

    for i in range(0, len(response["containedSpaces"])):
        if response["containedSpaces"][i]["name"] == buildingName:
            return(response["containedSpaces"][i]["id"])
    return "Invalid building name"


def listFloors(campus, buildingName):
    building_id = getBuildingID(campus, buildingName)
    r = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/" + building_id)
    response = r.json()
    output = []

    for i in range(0, len(response["containedSpaces"])):
        output.append(response["containedSpaces"][i]["name"])
    return output


def getFloorID(campus, buildingName, floor):
    building_id = getBuildingID(campus, buildingName)
    r = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/" + building_id)
    response = r.json()

    for i in range(0, len(response["containedSpaces"])):
        if response["containedSpaces"][i]["name"] == floor:
            return response["containedSpaces"][i]["id"]
    return "Invalid floor"


def listRooms(campus, buildingName, floor):
    floor_id = getFloorID(campus, buildingName, floor)
    r = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/" + floor_id)
    response = r.json()
    output = []

    for i in range(0, len(response["containedSpaces"])):
        output.append(response["containedSpaces"][i]["name"])
    return output


def getRoomID(campus, buildingName, floor, room):
    floor_id = getFloorID(campus, buildingName, floor)
    r = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/" + floor_id)
    response = r.json()

    for i in range(0, len(response["containedSpaces"])):
        if response["containedSpaces"][i]["name"] == room:
            return response["containedSpaces"][i]["id"]
    return "Invalid room"


def getRoomCapacity(campus, buildingName, floor, room):
    room_id = getRoomID(campus, buildingName, floor, room)
    r = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/" + room_id)
    response = r.json()

    return response["capacity"]["normal"]


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

    user = getUserByID(_userid)
    if user == None:
        return "-1"

    _users = "[ "

    checkedin = False

    tickets = Ticket.query()

    for ticket in tickets:
        if ticket.room == room:
            _users += '{{"username":"{}"}},'.format(ticket.user.username)
            if ticket.user == user:
                checkedin = True

    _users = _users[:-1] + "]"

    return """
            {{
                "name":"{}",
                "building":"{}",
                "campus":"{}",
                "occupancy":{},
                "capacity":{},
                "users":{},
                "checkedin":{}
            }}
        """.format(room.name, room.building, room.campus, room.occupancy, room.capacity, _users, "true" if checkedin else "false")


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


@app.get('/addroom')
def addroom():
    return


def userLoggedInTemplate(user):
    return template(usertemplate, user=user)


def adminLoggedInTemplate(adminscript):
    return template(admintemplate, username=adminscript)


if __name__ == '__main__':
    run(app, host='localhost', port=8080)
