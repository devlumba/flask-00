from flask import Flask, render_template, redirect, url_for, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "SECRET_KEY"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(hours=1)
db = SQLAlchemy(app)
#
# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()
#         app.run(debug=True)


# I will remake this whole shit, rn just following the tutorial even though the guy's insane
class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("username", db.String(100), unique=True, nullable=False)
    email = db.Column("email", db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


@app.route("/", methods=["GET"])
def get_slash():
    return render_template("elvel.html")


@app.route("/user/me")
def get_current_user():
    if "user" in session:
        user = session["user"]
        return redirect(url_for("get_user", user_id=user))
    else:
        return redirect(url_for('log_in'))


@app.route("/user/<user_id>")
def get_user(user_id):
    return render_template("usr.html", id=user_id)


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
            return redirect("/")
        flash("You successfully logged in", "info")
        return redirect(url_for('get_user', user_id=user))
    else:
        if "user" in session:
            flash("You already logged in", 'info')
            return redirect(url_for("get_current_user"))
    return render_template("login.html")


@app.route("/logout", methods=["GET", "POST"])
def log_out():
    if "email" in session:
        email = session["email"]
        name = session["name"]
        flash("You successfully have been logged out!", "info")
        session.pop("name", None)
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


