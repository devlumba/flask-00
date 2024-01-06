from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from .main import app
from datetime import timedelta
from .models import User



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


@app.route("/users")
def get_users():
    return render_template("users.html", users=User.query.all())


@app.route("/login", methods=["POST", "GET"])
def log_in():
    if request.method == "POST":
        # user = request.form["nm"]
        # session["user"] = user
        # # doesn't work when is unchecked for some reason
        # if request.form["remember"]:
        #     session.permanent = True
        found_user = User.query.filter_by(username=request.form["username"]).first()
        found_email = User.query.filter_by(email=request.form["email"]).first()
        if found_user or found_email:
            user = request.form["username"]
            email = request.form["email"]
            session["user"] = user
            session["email"] = email
            flash("You successfully signed in")
            return redirect(url_for("get_user", user=found_user.username))
        else:
            flash("Incorrect username of email")
            return redirect(url_for("log_in"))
    else:
        if "user" in session:
            flash("You already logged in", 'info')
            return redirect(url_for("get_current_user"))
    return render_template("login.html")


@app.route("/logout", methods=["GET", "POST"])
def log_out():
    if "email" in session:
        email = session["email"]
        user = session["user"]
        flash("You successfully have been logged out!", "info")
        session.pop("user", None)
        session.pop("email", None)
    else:
        flash("You aren't logged in", "info")
    return redirect("/")


@app.route("/signup", methods=["GET","POST"])
def sign_up():
    if "user" in session or "email" in session:
        flash("Log out first!", "info")
        return redirect("/")
    if request.method == "POST":
        # name = request.form["nm"]
        # email = request.form["email"]
        # session["name"] = name
        # session["email"] = email
        found_user = User.query.filter_by(username=request.form["username"]).first()
        found_email = User.query.filter_by(email=request.form["email"]).first()
        if found_user or found_email:
            flash("Username or email is already taken")
            return redirect(url_for("sign_up"))
        else:
            usr = User(username=request.form["username"], email=request.form["email"])
            with app.app_context():
                db.session.add(usr)
                db.session.commit()
        flash("You have successfully signed up!", "info")
        return redirect("/")
    return render_template("sign-up.html")

