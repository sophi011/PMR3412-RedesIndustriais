from flask import Flask, render_template, request, redirect, url_for, make_response, abort
from operator import itemgetter
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
    basedir, 'db.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()

@app.route('/')
def index():
    
    return render_template('index.html')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
            return '<User %r>' % self.name

@app.route('/signup/', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user = User(name=name,
                            email=email,
                            password=password)
        db.session.add(user)
        db.session.commit()
        response = make_response(redirect(url_for('index')))
        response.status_code = 201

        return response
    return render_template('signup.html')

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email, password=password).first()
        
        if user:
            user_cookie = str(user.id)
            response = make_response(redirect(url_for('index_logged')))
            response.set_cookie('user_auth', user_cookie)
            response.status_code = 200

            return response
        
        else:
            response = make_response(redirect(url_for('index_logged')))
            response.status_code = 401
            return response
                
    return render_template('login.html')

@app.route('/index_logged/', methods=['GET'])
def index_logged():
    user_cookie = request.cookies.get('user_auth')
    if user_cookie:
        user = User.query.filter_by(id = user_cookie).first()
        if user:
            return render_template('index_logged.html', user = user)

    abort(401)

@app.route('/logout/', methods=['POST', 'GET'])
def logout():
    if request.method == 'POST':
        res = make_response(redirect(url_for('index')))
        res.set_cookie('user_auth', 'logout', max_age=0)
        return res
                
    return render_template('logout.html')


"""
admin = User(name='admin', email='sophia.celine@hotmail.com', password='pass1')
db.session.add(admin)


db.session.commit()
"""
# export FLASK_APP=server
# python3 -m flask run

#flask shell

# https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application