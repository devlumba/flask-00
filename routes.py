import base64

from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import login_user, current_user, logout_user
from .main import app, db, bcrypt, login_manager
from datetime import timedelta
from .models import User
from .forms import MyForm, SignIn, SignUp


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.args.get('api_key')
    if api_key:
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        try:
            api_key = base64.b64decode(api_key)
        except TypeError:
            pass
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    return None


@app.route("/", methods=["GET"])
def get_slash():
    return render_template("elvel.html")


@app.route("/user/me")
def get_current_user():
    if "user" in session:
        user = session["user"]
        email = session["email"]
        return redirect(url_for("get_user", user=user))
    else:
        return redirect(url_for('log_in'))


@app.route("/user/<user>")
def get_user(user):
    return render_template("usr.html", user=user)


@app.route("/users/me")
def get_me():
    return render_template("users.html", user=current_user)


@app.route("/users")
def get_users():
    return render_template("users.html", users=User.query.all())


@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    form = SignIn()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            # I probably should add remember checkbox, then login_user(user, remember=form.remember.data)
            flash("You have logged successfully")
            return redirect(url_for("get_me", user=user))
        else:
            flash("Incorrect email or password")
            return redirect(url_for("sign_in"))
    return render_template("sign_in.html", form=form)


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    form = SignUp()
    if request.method == "POST":
        found_user = User.query.filter_by(email=form.email.data).first()
        if not found_user:
            hashed_password = generate_password_hash(form.password.data).decode("utf-8")
            with app.app_context():
                user = User(username=form.username.data, email=form.email.data, password=hashed_password)
                db.session.add(user)
                db.session.commit()
            flash("You have successfully signed up, now you can sign in.")
            return redirect(url_for("sign_in"))
        else:
            flash("Username/email taken")
            return redirect(url_for("sign_up"))
    return render_template("sign_up.html", form=form)



@app.route("/log_out", methods=["GET", "POST"])
def log_out():
    logout_user()
    return redirect("/")


@app.route("/check_form", methods=["GET", "POST"])
def test_form():
    form = MyForm()
    if form.validate_on_submit():
        flash("Successfully filled form")
        return redirect("/users")
    return render_template("test_form.html", form=form)
#
#
# with app.app_context():
#     db.create_all()
#     user = User(username='username', email='email@gmail.com', password='username')
#     db.session.add(user)
#     db.session.commit()