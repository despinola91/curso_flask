from flask import Flask, request, make_response, redirect, render_template, session
#from flask_bootstrap import Bootstrap
from flask_bs4 import Bootstrap
from os import urandom

app = Flask(__name__)
bootstrap = Bootstrap(app) #Inicializamos bootstrap

app.config['SECRET_KEY'] = 'SUPER SECRETO'
#app.config['SECRET_KEY'] = urandom(16) --> forma más segura de generar secret key


todos = ['Comprar café', 'Enviar solicitud de compra', 'Entregar video al productor']

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html', error=error)


@app.route('/')
def index():
    user_ip = request.remote_addr

    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip

    return response


@app.route('/hello')
def hello():
    user_ip = session.get('user_ip')
    context = {
        'user_ip':user_ip,
        'todos': todos
    }
    #return render_template('hello.html', user_ip=user_ip, todos=todos)
    return render_template('hello.html', **context)


