import sqlite3
import uuid
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
DB_NAME = 'bank_app.db'
active_sessions={}

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    session_id = request.args.get('session')
    if session_id and session_id in active_sessions:
        return render_template('dashboard.html',username=active_sessions[session_id]['user_name'])
    return redirect(url_for('home'))

def create_session(account_id,user_name):
    session_id = str(uuid.uuid4())
    active_sessions[session_id] = {'account_id':account_id,'user_name':user_name}
    return session_id

@app.route('api/v1/signup',methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    nominee_name = data.get('nominee_name')
    nominee_relation = data.get('nominee_relation')

    if not all([username,password,nominee_name,nominee_relation]):
        return jsonify({"error":"Missing required fields"}),400
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    conn = get_db_connection()

    try:
        cursor = conn.execute(
            "INSERT INTO accounts (username, password_hash) VALUES (?,?)",
            (username,password_hash)
        )
        account_id = cursor.lasrrowid
        conn.execute(
            "INSERT INTO nominees (account_id, full_name,relation) VALUES (?,?,?),",
            (account_id,nominee_name,nominee_relation)
        )
        conn.commit()
        return jsonify({"message":"Account created successfully"},201)
    except sqlite3.IntegrityError:
        return jsonify({"error":"user_name already exists"},409)
    finally:
        conn.close()







