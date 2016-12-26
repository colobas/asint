from bottle import Bottle, template
import fenixedu

app=Bottle()

@app.route('/spaces')
def greet(name=''):
    return template('Hello {{name}}, how are you?', name=name)

if __name__ == '__main__':
    run(app, host = https://fenix.tecnico.ulisboa.pt/api/fenix/v1, port = 8000)