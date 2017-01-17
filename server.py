# coding=utf-8

"""
O browser fala com o servidor através de pedidos HTTP. Para tal utiliza-se JavaScript.
O JS serve para a página não ter de ser actualizada sempre que se faz algum pedido.
Cada vez que se faz um pedido, o browser envia-o por HTTP ao servidor, que responde com o resultado do pedido.
Quando um pedido é enviado ao servidor, ele recebe-o, processa-o e retorna o resultado.
Consoante a resposta recebida pelo browser, este corre uma tarefa/função específica (JS).

"""

from bottle import Bottle, run, template, request
from user import User
import base64, requests, hashlib
from room import Room
from ticket import Ticket
import json

app = Bottle()

# Dict com utilizadores registados, para teste
users = dict()
andre = User("andre")
miguel = User("miguel")

users[andre.id] = andre
users[miguel.id] = miguel

rooms = dict()
room1 = Room(12,"sala1", "alameda", "edificio1", 10, 0)
room2 = Room(13,"sala2", "tagus", "edificio2", 12, 0)
rooms[room1.id] = room1
rooms[room2.id] = room2

tickets = dict()



def add_room(campus, building, floor, room_name):
    sha1 = hashlib.sha1()
    sha1.update(room_name.encode('utf-8'))
    digest = sha1.hexdigest()[0:5]
    room_id = int(digest, 16)
    capacity = getRoomCapacity(campus, building, floor, room_name)
    occupancy = 0

    new_room = Room(room_id, room_name, campus, floor, capacity, occupancy)
    rooms[new_room.id] = new_room

def check_in(user_id, room_name):
    for key in rooms:
        if room_name == rooms[key].name:
            room_id = rooms[key].id

    for key in reg_users.keys():
        if user_id == key:
            username = reg_users[key].username

    new_ticket = Ticket(room_id, username)
    tickets[user_id] = new_ticket
    print(tickets[772480].username)

usertemplate = ""
with open("user_template.st", "r") as f:
    usertemplate = f.read()


# Index, o que aparece no browser quando se acede ao servidor
@app.route('/')
def home():
    check_in(772480, "sala1")
    return template(
        """
        <!--COMMENT: Tudo o que está em HTML é estático. São os elementos que aparecem no browser-->
        <html>
            <head>
            <p id="register"></p>

            <!--COMMENT: Script JS, responsável por tudo o que é dinâmico-->
            <script>

                // Função que submete para o servidor o username inserido e faz o login ou registo
                //  Recebe como argumento "reg" ou "log", dependendo do botao clicado

                function submit(mode) {

                    // str guarda o username introduzido, do respectivo campo login/registo-->

                    if(mode=="reg"){
                        var str = document.getElementById("username_reg").value;
                    }else{
                        var str = document.getElementById("username_log").value
                    }

                    var xmlhttp = new XMLHttpRequest();

                    //Espera pela resposta. Quando é recebida, corre a função, e faz o que tem a fazer de acordo com a resposta recebida

                    xmlhttp.onreadystatechange = function() {

                        if (this.readyState == 4 && this.status == 200) {

                            //Divide a resposta do servidor em username e id

                            var response = xmlhttp.responseText.split(",");
                            if (response != "0") {
                                window.location = "/user/"+response
                            } else {
                                window.location = "/admin"
                            }
                        }
                    }

                    // Envia o nome introduzido e o modo (log ou reg) para o servidor (app.post('/'))
                    xmlhttp.open("POST", "/", true);
                    xmlhttp.send("data="+str+","+mode);
                }

            </script>
            </head>
            <body>
                <center><h1>Login</h1>
                    Username:<br>
                    <input method="post" id="username_log" type="text" />
                    <br>
                    <button onclick="submit('log')">Login</button>
                <br><br>
                <center><h3>Register</h3>
                    Username:<br>
                    <input method="post" id="username_reg" type="text" />
                    <br>
                    <button onclick="submit('reg')">Register</button>
                </center>
            </body>
        </html>
        """)


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

    # REG - Se nao houver ninguém registado, cria novo utilizador, e regista-o
    # LOG - Se não houver ninguém registado, impossível fazer login
    if len(users) == 0:
        if mode == "reg":
            new_user = User(username)
            users[new_user.id] = new_user
            return str(new_user.id)
        elif mode == "log":
            return "invalid_log"

    # REG - Caso existam users registados, se o nome introduzido já existir, impossível registar
    # LOG - Se o nome introduzido já estiver registado, devolve username e id.
    for id, user in users.items():
        if username == user.username:
            if mode == "log":
                return str(id)
            elif mode == "reg":
                return "invalid_reg"

    # LOG - Se o nome introduzido não estiver registado, impossível fazer login
    if mode == "log":
        return "invalid_log"
    # REG - Se o nome introduzido não estiver registado, regista-o e devolve username e id
    elif mode == "reg":
        new_user = User(username)
        users[new_user.id] = new_user
        return str(new_user.id)


@app.route('/user/<userid>')
def user(userid):
    _id = int(userid)
    if _id in users:
        return userLoggedInTemplate(users[_id])
    else:
        return "no such user"


@app.get('/listrooms')
def listrooms():

    response = "["

    for room in rooms.values():
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

@app.get('/room/<roomid>/<userid>')
def roomview(roomid, userid):
    _roomid = int(roomid)
    _userid = int(userid)
    room = rooms[_roomid] # TODO: criar dicionario rooms
    _users = "[ "

    checkedin = False


    for ticket in tickets.values():
        if ticket.roomid == _roomid:
            _users += '{{"username":"{}"}},'.format(users[ticket.user].username)
            if ticket.user == _userid:
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

    if _roomid in rooms and _userid in users:
        room = rooms[_roomid]
        if room.occupancy + 1 <= room.capacity:
            tickets[_userid] = Ticket(_roomid, users[_userid])
            room.occupancy += 1

    return ""

@app.get('/checkout/<userid>')
def checkout(userid):
    _userid = int(userid)

    if _userid in users:
        if _userid in tickets:
            room = rooms[tickets[_userid].roomid]
            room.occupancy -= 1
            del tickets[_userid]

    return ""


@app.route('/admin')
def admin():
    return adminLoggedInTemplate("")



def userLoggedInTemplate(user):
    return template(usertemplate, user=user)


def adminLoggedInTemplate(adminscript):
    return ""


if __name__ == '__main__':
    run(app, host='localhost', port=8080)
