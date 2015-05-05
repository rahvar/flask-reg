from app import app,db
from flask import request,redirect,url_for,render_template,session,flash,g
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm,RegistrationForm
from models import User


@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/register',methods = ["GET","POST"] )
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash("Thanks for registering!")
        
        username = form.username.data
        email = form.email.data
        password = form.password.data

        user = User(username = username,email= email,password=password)
   
        db.session.add(user)
        db.session.commit()

        session['logged_in'] = True
        session['username'] = username
       
        return  redirect(url_for('user',username = username))
    print "hey"
    return render_template("register.html", form = form)

@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username = username).first()
    if user is None:
        flash('User %s not found.' % username)
        return redirect(url_for('home'))
    return render_template("user.html",user= user)

@app.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("logged in")
