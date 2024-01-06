from flask import Blueprint, render_template, redirect, url_for

second = Blueprint("admin", __name__, static_folder="static", template_folder="templates")


@second.route("/blueprint")
def slash():
    return render_template("elvel.html")
