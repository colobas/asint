# coding=utf-8

"""
O browser fala com o servidor através de pedidos HTTP. Para tal utiliza-se JavaScript.
O JS serve para a página não ter de ser actualizada sempre que se faz algum pedido.
Cada vez que se faz um pedido, o browser envia-o por HTTP ao servidor, que responde com o resultado do pedido.
Quando um pedido é enviado ao servidor, ele recebe-o, processa-o e retorna o resultado.
Consoante a resposta recebida pelo browser, este corre uma tarefa/função específica (JS).

"""

from bottle import Bottle, run, template, request
import user

app = Bottle()

# Dict com utilizadores registados, para teste
reg_users = {"1234": "andre", "349857": "miguel"}


# Index, o que aparece no browser quando se acede ao servidor
@app.route('/')
def home():
    return template(
        """
        <!--COMMENT: Tudo o que está em HTML é estático. São os elementos que aparecem no browser-->
        <html>
            <head>
            <p id="register"></p>

            <!--COMMENT: Script JS, responsável por tudo o que é dinâmico-->
            <script>

                <!--COMMENT: Função que submete para o servidor o username inserido e faz o login ou registo-->
                <!--COMMENT: Recebe como argumento "reg" ou "log", dependendo do botao clicado-->

                function submit(mode) {

                    <!--COMMENT: str guarda o username introduzido, do respectivo campo login/registo-->

                    if(mode=="reg"){
                        var str = document.getElementById("username_reg").value;
                    }else{
                        var str = document.getElementById("username_log").value
                    }

                    var xmlhttp = new XMLHttpRequest();

                    <!--COMMENT: Espera pela resposta. Quando é recebida, corre a função, e faz o que tem a fazer de acordo com a resposta recebida-->

                    xmlhttp.onreadystatechange = function() {

                        if (this.readyState == 4 && this.status == 200) {

                            <!--COMMENT: Divide a resposta do servidor em username e id-->

                            var response = xmlhttp.responseText.split(",");
                            username = response[0];
                            id = response[1];

                            <!--COMMENT: Nome de registo invalido, retorna mensagem de alerta-->

                            if(username == "invalid_reg"){
                                window.alert("Username already taken. Please choose another one.");

                            <!--COMMENT: Nome de login invalido, retorna mensagem de alerta-->

                            }else if(username == "invalid_log"){
                                window.alert("User not registered.");

                            <!--COMMENT: Caso tudo corra bem, no registo, sao apresentados o nome e id que foram registados-->
                            <!--COMMENT: Caso tudo corra bem, no login, username e id sao armazenados numa cookie e a pagina é redireccionada para a página de login-->

                            }else{
                                if(mode=="reg"){
                                    document.getElementById("register").innerHTML = "Registered as " + username + "<br>ID: " + id;
                                }else{
                                    document.cookie = response;
                                    window.location = "/login"
                                }
                            }
                        }
                    }

                    <!--COMMENT: Envia o nome introduzido e o modo (log ou reg) para o servidor (app.post('/'))-->

                    xmlhttp.open("POST", "", true);
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


@app.post('/')
def home():

    # Dados enviados pelo browser
    # Divididos em username e mode (reg ou log)
    data = request.forms.get('data').split(",")
    username = data[0]
    mode = data[1]

    # import pdb; pdb.set_trace()
    # Se o user for admin, retorna com id 0
    if username == "admin":
        return "admin,0"

    # REG - Se nao houver ninguém registado, cria novo utilizador, e regista-o
    # LOG - Se não houver ninguém registado, impossível fazer login
    if len(reg_users) == 0:
        if mode == "reg":
            new_user = user.User(username)
            reg_users[new_user.getId()] = new_user.getUsername()
            return new_user.getUsername() + "," + new_user.getId()
        elif mode == "log":
            return "invalid_log"

    # REG - Caso existam users registados, se o nome introduzido já existir, impossível registar
    # LOG - Se o nome introduzido já estiver registado, devolve username e id.
    for key, value in reg_users.items():
        if username == value:
            if mode == "log":
                return value + "," + key
            elif mode == "reg":
                return "invalid_reg"

    # LOG - Se o nome introduzido não estiver registado, impossível fazer login
    if mode == "log":
        return "invalid_log"

    # REG - Se o nome introduzido não estiver registado, regista-o e devolve username e id
    elif mode == "reg":
        new_user = user.User(username)
        reg_users[new_user.getId()] = new_user.getUsername()
        return new_user.getUsername() + "," + new_user.getId()


@app.route('/login')
def login():
    return template("""
        <html>
            <head>
                    <p id="login"></p>
                <center>
                    <h1 id="admin" style="display: none">Admin</h1>
                    <h1 id="student" style="display: none">Student</h1>

                </center>

                <script>

                    var data = document.cookie.split(",");
                    username = data[0];
                    id = data[1];

                    document.getElementById("login").innerHTML = "Logged in as " + username + "<br>ID: " + id;

                    function display_(id, displayValue){
                        if ( displayValue == 1 ) {
                            document.getElementById(id).style.display = 'block';
                        } else if ( displayValue == 0 ) {
                            document.getElementById(id).style.display = 'none';
                        }
                    }

                    if(username == 'admin'){
                        display_('admin', 1);
                    }else{
                        display_('student', 1);
                    }


                </script>
            </head>
            <body>

            </body>
        </html>
        """)


@app.post('/login')
def login():
    return


if __name__ == '__main__':
    run(app, host='localhost', port=8080)
