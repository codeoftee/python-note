from flask import render_template, request, flash, session
import hashlib
from app import app, db
from app.models import User

@app.route('/')
def index():
    logged_in = False
    if 'name' in session:
        logged_in = True
        name = session['name']
        email = session['email']
    else:
        name = None
        email = None
    return render_template('index.html', name=name, email=email, logged_in=logged_in)


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form['email']
        password = request.form['password']
        print('Submitted email ' + str(email))
        print('Submitted password ' + str(password))
        # hash submitted password
        password_hash = hashlib.sha256(password.encode())
        hashed = password_hash.hexdigest()

        # query the database for hashed password and email
        user = User.query.filter((User.email == email) & (User.password_hash == hashed)).first()

        if user is None:
            flash("Invalid email or password!")
            return render_template('login.html')
        else:
            # python sessions https://pythonbasics.org/flask-sessions/
            session['name'] = user.name
            session['email'] = user.email
            return render_template('welcome.html', name=user.name)


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
        user = User(name=name, email=email, phone=phone, password_hash=hashed)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful!")
        return render_template('welcome.html', name=user.name)


@app.route('/test')
def add_user():
    u = User(name='Queen', email='queen@example.com', phone='0809988776676', password_hash='pass_hash')
    db.session.add(u)
    db.session.commit()
    return u.name + ' Added'
