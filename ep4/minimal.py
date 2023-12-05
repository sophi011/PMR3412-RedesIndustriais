from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
    basedir, 'db.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

"""
from database_test import User, db
admin = User(username='admin', email='admin@example.com')
guest = User(username='guest', email='guest@example.com')
db.session.add(admin)
db.session.add(guest)
db.session.commit()
Para a leitura de dados, temos as seguintes funções principais:

User.query.all() # obtem todos as entradas de user
User.query.get(2) # obtem usuario com id igual a 2
user = User.query.filter_by(email='fulano@usp.br').first() 
# obtem o usuario com o email fulano@usp.br ou None se nao encontrar
user = User.query.filter_by(email='fulano@usp.br').first_or_404(description=f'There is no user with email fulano@usp.br') 
# o mesmo que o anterior mas invoca 404 se nao encontrar
"""