"""Blogly application."""

from flask import Flask, render_template, redirect
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
    return redirect("/users")


@app.route("/users")
def show_users():
    users = User.query.all()
    return render_template("user_listing.html", users=users)


@app.route("/users/new")
def show_new_user_form():
    return render_template("user_new.html")

@app.route("/users/new", methods=["POST"])
def redirect_to_home():
    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user_details(user_id):
    user = User.query.filter(User.id == user_id).one()
    # print("THIS IS MY USERNAME", user.first_name)

    return render_template("user_detail.html", user=user)

# @app.route("/users/<int:id>/edit")

# @app.route("/users/<int:id>/edit", methods=["POST"])

# @app.route("/users/<int:id>/delete", methods=["POST"])
