from bottle import Bottle, run, template, request
import user

app=Bottle()

reg_users = {"1234" : "andre", "349857" : "miguel"}

@app.route('/')
def home():
	return template(
        """
        <html>
            <head>
            <script>
                function send_form() {
                    var str = document.getElementById("username").value;
                    var xmlhttp = new XMLHttpRequest();

                    xmlhttp.onreadystatechange = function() {
                        if (this.readyState == 4 && this.status == 200) {
                        var response = xmlhttp.responseText;
                            if(response == "no"){
                                window.alert("Username already taken. Please choose another one.");
                            }
                        }
                    }

                    xmlhttp.open("POST", "", true);
                    xmlhttp.send("username="+str);
                }
            </script>
            </head>
            <body>
                <center><h1>Login</h1>
                    Username:<br>
                    <input id="username" type="text" />
                <button onclick="send_form()">Login</button>
                </center>
            </body>
        </html>
        """)

@app.post('/')
def login():


    username = request.forms.get('username')

    if len(reg_users) == 0:
        new_user = user.User(username)
        reg_users[new_user.getId()] = new_user.getUsername()
        return template(
            """
            <ul>
                %for id, name in list:
                 <li>{{(name, id)}}</li>
                %end
            </ul>""", list=reg_users.items())

    for name in reg_users.values():
        if username == name:
            #import pdb; pdb.set_trace()
            return "no"

    new_user = user.User(username)
    reg_users[new_user.getId()] = new_user.getUsername()
    return template(
        """
        <ul>
           %for name in list:
            <li>{{name}}</li>
           %end
        </ul>""", list=reg_users)


if __name__ == '__main__':
    run(app, host = 'localhost', port = 8080)