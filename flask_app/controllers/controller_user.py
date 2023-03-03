from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.model_user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import flash

@app.route('/register')
def user_register():
    return render_template("user_register.html")

@app.route('/register', methods = ['POST'])
def user_create():
    if User.validate(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)
        data = {
            **request.form,
            'password': pw_hash,
        }
        id = User.create(data)
        print(id)
        session['id'] = id
        session['user_name'] = request.form['first_name']
        return redirect('/books/dashboard')
    return redirect('/register')

@app.route('/login', methods=["POST"])
def user_login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Email/Password")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid Email/Password')
        return redirect('/')
    session['id'] = user.id
    session['user_name'] = user.first_name
    return redirect('/books/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')