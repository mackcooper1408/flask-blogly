"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User, Post
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension


@app.route("/")
def start():
    return redirect("/users")


@app.route("/users", strict_slashes=False)
def show_users():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("user_listing.html", users=users)


@app.route("/users/new")
def show_new_user_form():
    return render_template("user_new.html")


@app.route("/users/new", methods=["POST"])
def process_new_user():

    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url']
    image_url = image_url if image_url else "https://bit.ly/3lUJbon"

    User.create_user(first_name, last_name, image_url)

    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user_details(user_id):
    user = User.query.get_or_404(user_id)
    # print("THIS IS MY USERNAME", user.first_name)

    return render_template("user_detail.html", user=user)


@app.route("/users/<int:user_id>/edit")
def edit_user_details(user_id):
    user = User.query.get_or_404(user_id)

    return render_template("user_edit.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def process_edit_user(user_id):
    user = User.query.get_or_404(user_id)

    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["image-url"]
    image_url = image_url if image_url else "https://bit.ly/3lUJbon"

    user.update_user(first_name, last_name, image_url)

    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def process_delete_user(user_id):
    user = User.query.get_or_404(user_id)

    user.delete_user(user)

    return redirect("/users")


@app.route("/users/<int:user_id>/posts/new")
def show_new_post_form(user_id):
    user = User.query.get_or_404(user_id)

    return render_template("post_new.html", user=user)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def process_post_form(user_id):

    title = request.form['title']
    content = request.form['content']

    Post.create_post(title, content, user_id)

    return redirect(f"/users/{user_id}")


# @app.route("/posts/<int:post_id>")
# @app.route("/posts/<int:post_id>/edit")
# @app.route("/posts/<int:post_id>/edit", methods=["POST"])
# @app.route("/posts/<int:post_id>/delete", methods=["POST"])
