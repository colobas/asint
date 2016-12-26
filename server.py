from bottle import Bottle, run, template, request, response
import student

app=Bottle()

reg_students = [];
reg_students.append(student.Student('andre'))

reg_admins = [];

@app.route('/')
def home():
	return template("""<style>
                            button{
                            width: 150;
                            height: 60;
                            display:inline-block;
                            }
                        </style>
                        <body>
                        <center>
                            <h1>Register</h1>
                            <button onclick="onClick()"><h3>Administrator</h3></button>
                            <button onclick="onClick()"><h3>Student</h3></button>
                            <script>
                                function onClick() {
                                document.location.href = 'http://localhost:8080/student';
                                }
                            </script>
                            <h1>Login</h1>
                            <button onclick="onClick()"><h3>Administrator</h3></button>
                            <button onclick="onClick()"><h3>Student</h3></button>
                            <script>

                            </script>
                        </center>
                        </body>""")

@app.route('/admin')
def admin():
    return

@app.get('/student')
def login_form():
    return '''<center><h1>Student</h1>
              <form method="POST" action="/student">
                Username:<br>
                <input name="username" type="text" />
                <input type="submit" />
              </form>
              </center>'''

@app.post('/student')
def submit_form():
    username = request.forms.get('username')
    print username

    if reg_students == []:
        reg_students.append(student.Student(username))
        return ''

    for i in reg_students:
        if username == i.username:
            response.status = 303
            response.set_header('Location', '/student')
            return
        else:
            reg_students.append(student.Student(username))
            return template(""" <ul>
                   %for name in list:
                    <li>{{name}}</li>
                   %end
                </ul>""", list=reg_students)


if __name__ == '__main__':
    run(app, host = 'localhost', port = 8080)