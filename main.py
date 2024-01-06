from flask import Flask, render_template, redirect, url_for, request, session, flash
# from flask_login import LoginManager, login_user
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from .admin.second import second

app = Flask(__name__)
app.secret_key = "SECRET_KEY"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(hours=1)
app.register_blueprint(second, url_prefix="/admin")
db = SQLAlchemy(app)

from . import routes

# login_manager = LoginManager()
# login_manager.init_app(app)
#
# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()
#         app.run(debug=True)


