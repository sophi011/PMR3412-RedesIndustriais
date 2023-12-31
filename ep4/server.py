from flask import Flask, render_template, request, redirect, url_for, make_response, abort
from flask_sqlalchemy import SQLAlchemy
import os
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend
import base64
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import hmac

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
    password_salt = db.Column(db.String(80), nullable=False)

    def __repr__(self):
            return '<User %r>' % self.name
    
class Session(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
            return '<Session %r>' % self.id

def hash_password(password, password_salt):
    salt = password_salt
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1, backend=default_backend())
    digest = kdf.derive(password.encode('utf-8'))
    key = base64.urlsafe_b64encode(digest)
    return key.decode('utf-8')

@app.route('/signup/', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        password_salt = os.urandom(16)
        password = hash_password(password, password_salt)
        password_salt = base64.urlsafe_b64encode(password_salt).decode('utf-8')
        user = User(name=name,
                    email=email,
                    password=password,
                    password_salt=password_salt)
        db.session.add(user)
        db.session.commit()
        response = make_response(redirect(url_for('index')))
        response.status_code = 201

        return response
    return render_template('signup.html')

def decrypt(aes, iv, text):
    aes_context = Cipher(algorithms.AES(aes), modes.CTR(iv), backend=default_backend())
    decryptor = aes_context.decryptor()
    decrypted_text = decryptor.update(text) + decryptor.finalize()
    return decrypted_text

def validate_hmac(mac, data, hmac_data):
    hash = hashes.Hash(hashes.SHA256(), backend=default_backend())
    hash.update(mac+data)
    hmac_calc = hash.finalize()
    validation = hmac.compare_digest(hmac_calc, hmac_data)
    return validation

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session_keys = request.form.get('session_keys')
        print("session_keys: ", session_keys)
        session_keys = base64.b64decode(session_keys)
        aes = session_keys[:32]
        mac = session_keys[32:64]
        iv = session_keys[64:]
        cyphertext = request.form.get('cyphertext')
        print("cyphertext: ", cyphertext)
        cyphertext = base64.b64decode(cyphertext)
        hmac_data = request.form.get('hmac')
        print("hmac: ", hmac)
        hmac_data = base64.b64decode(hmac_data)
        
        
        mac_validation = validate_hmac(mac, cyphertext, hmac_data)
        if not mac_validation:
            abort(401)

        decrypted_data = decrypt(aes, iv, cyphertext).decode()
        email, password = decrypted_data.split(":")
        user = User.query.filter_by(email=email).first()
        
        if user:
            if user.password == hash_password(password, base64.urlsafe_b64decode(user.password_salt.encode('utf-8'))):
                response = make_response(redirect(url_for('index_logged')))
                random_number = os.urandom(16)
                session_hash = hashlib.md5(random_number).hexdigest()
                new_session = Session(id=session_hash, user_id=user.id)
                db.session.add(new_session)
                db.session.commit()
                response.set_cookie('session_id', new_session.id)
                response.status_code = 200

                return response
            
            print("Fail!")
            response = make_response(redirect(url_for('index_logged')))
            response.status_code = 401
            abort(401)
        
        else:
            response = make_response(redirect(url_for('index_logged')))
            response.status_code = 401
            return response
                
    return render_template('login.html')

@app.route('/index_logged/', methods=['GET'])
def index_logged():
    session_cookie = request.cookies.get('session_id')
    if session_cookie:
        session = Session.query.filter_by(id = session_cookie).first()
        if session:
            user = User.query.filter_by(id=session.user_id).first()
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

db.session.commit()
"""
# export FLASK_APP=server
# python3 -m flask run

#flask shell

# https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application