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
            <!--COMMENT: Script JS, responsável por tudo o que é dinâmico-->
            <script>

                <!--COMMENT: Função para fazer o login e verificação dos usernames-->

                function login() {

                    <!--COMMENT: str guarda o username introduzido-->

                    var str = document.getElementById("username").value;
                    var xmlhttp = new XMLHttpRequest();

                    <!--COMMENT: Espera pela resposta. Quando é recebida, corre a função, e faz o que tem a fazer
                        de acordo com a resposta recebida-->

                    xmlhttp.onreadystatechange = function() {

                        if (this.readyState == 4 && this.status == 200) {

                            var response = xmlhttp.responseText;

                            <!--COMMENT: Se o username já existir, retorna mensagem de alerta-->
                            if(response == "invalid_username"){
                                window.alert("Username already taken. Please choose another one.");

                            <!--COMMENT: Se o username for "admin", vai para a página de admin-->
                            }else if(response == "admin"){
                                window.location = "/admin";

                            <!--COMMENT: Caso contrário, regista o novo aluno e vai para a página de aluno-->
                            }else{
                                window.location = "/student?username="+str;
                            }
                        }
                    }

                    <!--COMMENT: Envia o nome introduzido (POST) para o servidor (app.post('/'))-->

                    xmlhttp.open("POST", "", true);
                    xmlhttp.send("username="+str);
                }
            </script>
            </head>
            <body>
                <center><h1>Login</h1>
                    Username:<br>
                    <input method="post" id="username" type="text" />
                <button onclick="login()">Login</button>
                </center>
            </body>
        </html>
        """)


@app.post('/')
def login():

    # Username que foi inserido pelo user e enviado pelo browser
    username = request.forms.get('username')

    #----------------
    #     Admin
    #----------------

    #import pdb; pdb.set_trace()

    if username == "admin":
        return "admin"

    # ----------------
    #     Student
    # ----------------

    # Se nao houver ninguém registado, cria novo utilizador, e regista-o
    if len(reg_users) == 0:
        new_user = user.User(username)
        reg_users[new_user.getId()] = new_user.getUsername()
        return "student"

    # Caso já haja utilizadores registados, percorre o dict e vê se há alguem que ja tenho um username igual
    # Caso sim, retorna "invalid_username" para o browser
    for name in reg_users.values():
        if username == name:
            return "invalid_username"

    # Caso não exista ninguem com o nome introduzido, cria um novo utilizador e regista-o
    new_user = user.User(username)
    reg_users[new_user.getId()] = new_user.getUsername()
    return "student"

#Pagina para os administradores
@app.route('/admin')
def admin():
    return template("""
        <h1>Admin</h1>
        """)


#Pagina para os estudantes
@app.route('/student')
def admin():
    print(request.query.get('username'))
    return template("""
        <h1>Student</h1>
        """)


if __name__ == '__main__':
    run(app, host='localhost', port=8080)
