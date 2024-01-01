from flask import Flask, render_template, redirect, url_for, request, session, flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "SECRET_KEY"
app.permanent_session_lifetime = timedelta(hours=1)

# if __name__ == "__main__":
#     app.run(debug=True)


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
        user = request.form["nm"]
        session["user"] = user
        # doesn't work when is unchecked for some reason
        if request.form["remember"]:
            session.permanent = True
        return redirect(url_for('get_user', user_id=user))
    else:
        if "user" in session:
            flash("You already logged in", 'info')
            return redirect(url_for("get_current_user"))
    return render_template("login.html")


@app.route("/logout", methods=["GET", "POST"])
def log_out():
    session.pop("user", None)
    return redirect("/")
