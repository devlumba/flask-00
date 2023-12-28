from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

# if __name__ == "__main__":
#     app.run()


@app.route("/")
def get_slash():
    return render_template("elvel.html")


@app.route("/user/<user_id>")
def get_user(user_id: int):
    return render_template("usr.html", id=user_id)
