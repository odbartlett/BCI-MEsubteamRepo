from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, mongo
from app.models import User

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = mongo.db.users.find_one({"username": username})
        if user and check_password_hash(user['password'], password):
            user_obj = User(username, password, user['_id'])
            user_obj._id = user['_id']
            login_user(user_obj)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        text = request.form.get('text')
        mongo.db.submissions.insert_one({'user_id': current_user.get_id(), 'text': text})
        flash('Submission successful')
    submissions = mongo.db.submissions.find({'user_id': current_user.get_id()})
    return render_template('dashboard.html', submissions=submissions)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        existing_user = mongo.db.users.find_one({"username": username})
        if existing_user is None:
            hashpass = generate_password_hash(password)
            mongo.db.users.insert_one({'username': username, 'password': hashpass})

            flash('Registration successful')
            return redirect(url_for('login'))
        flash('Username already exists')
    return render_template('register.html')

