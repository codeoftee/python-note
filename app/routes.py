from flask import render_template, request, flash
import hashlib
from app import app, db
from app.models import User

user_profile = {
    'name': 'Israel',
    'email': 'test@test.com',
    'password': 'mySecret'
}

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form['email']
        password = request.form['password']
        print('Submitted email ' + str(email))
        print('Submitted password ' + str(password))
        if email == user_profile['email'] and password == user_profile['password']:
            return render_template('welcome.html', name=user_profile['name'])
        else:
            flash('Invalid username and password!')
            return render_template('login.html')


@app.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        email = request.form['email']
        print('email is {}'.format(email))
        name = request.form['name']
        phone = request.form['phone']
        if name == '' or phone == '':
            flash('Please enter your name and phone number')
            return render_template('signup.html')
        gender = request.form['gender']
        if gender == '':
            flash('Please select gender!')
            return render_template('signup.html')
        password = request.form['password']
        password2 = request.form['password2']
        if password == '':
            flash('Please enter your password.')
            return render_template('signup.html')
        if password != password2:
            flash('Passwords does not match!')
            return render_template('signup.html')
        # "Signup success"
        password_hash = hashlib.sha256(password.encode())
        hashed = password_hash.hexdigest()
        user = User(name=name, email=email, phone=phone, password_hash=password)
        db.session.add(user)
        db.session.commit()
        return "You have been registered successfully! {}".format(name)


@app.route('/test')
def add_user():
    u = User(name='Queen', email='queen@example.com', phone='0809988776676', password_hash='pass_hash')
    db.session.add(u)
    db.session.commit()
    return u.name + ' Added'
