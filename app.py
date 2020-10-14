"""Blogly application."""

from flask import Flask, render_template
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

toolbar = DebugToolbarExtension


@app.route("/")
def start():
    users = User.query.all()
    return render_template("user_listing.html", users=users)


# @app.route("/users")
# def show_users():
#     users = User.query.all()
#     return render_template("user_listing.html", users=users)

# @app.route("/users/new")

# @app.route("/users/new", methods=["POST"])

# @app.route("/users/<int:id>")

# @app.route("/users/<int:id>/edit")

# @app.route("/users/<int:id>/edit", methods=["POST"])

# @app.route("/users/<int:id>/delete", methods=["POST"])
