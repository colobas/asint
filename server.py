from bottle import Bottle, run, template, request, response
import user

app=Bottle()


reg_users = {"1234" : "andre", "349857" : "miguel"}

@app.route('/')
def home():
	return template(

    """<center><h1>Login</h1>
                              <form name="login_form" method="post">
                                Username:<br>
                                <input name="username" type="text" />
                              </form>
                              <button onclick="send_form()">Login</button>
                                <script>
                                    function send_form() {
                                        document.login_form.submit();
                                    }
                                </script>
                        </center>""")

@app.post('/')
def login():
    username = request.forms.get('username')

    if len(reg_users) == 0:
        new_user = user.User(username)
        reg_users[new_user.getId()] = new_user.getUsername()
        return template(""" <ul>
                   %for id, name in list:
                    <li>{{(name, id)}}</li>
                   %end
                </ul>""", list=reg_users.items())

    for name in reg_users.values():
        #import pdb; pdb.set_trace()
        if username == name:
            response.status = 303
            response.set_header('Location', '/student')
            return

    new_user = user.User(username)
    reg_users[new_user.getId()] = new_user.getUsername()
    return template(""" <ul>
           %for name in list:
            <li>{{name}}</li>
           %end
        </ul>""", list=reg_users)



if __name__ == '__main__':
    run(app, host = 'localhost', port = 8080)