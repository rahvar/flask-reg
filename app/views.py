from app import app,db,lm
from flask import request,redirect,url_for,render_template,session,flash,g
from flask.ext.login import login_user, logout_user, current_user
from forms import LoginForm,RegistrationForm
from models import User
from functools import wraps

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login_page'))

    return wrap

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

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
        g.user = current_user
        session['logged_in'] = True
        session['username'] = username
       
        return  redirect(url_for('user',username = username))
    print "hey"
    return render_template("register.html", form = form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username = username).first()
    if user is None:
        flash('User %s not found.' % username)
        return redirect(url_for('home'))
    return render_template("user.html",user= user)

@app.route('/login',methods = ["GET","POST"])
def login():
    form = LoginForm()
    error = ''
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('home'))
    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username = username).first()
        if user is not None:
            print user.password,form.password.data
            if user.password == form.password.data:
                print "hey"
                session['logged_in'] = True
                session['username'] = username
                flash("logged in")
                g.user = current_user
                return redirect(url_for('user',username = username))
            else:
                error = "Incorrect password"    
        else:
            error = "Invalid credentials, try again"
    return render_template("login.html",form=form,error = error)

@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('home'))