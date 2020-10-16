"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User, Post, Tag, PostTag
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension


""" HOME ROUTE """

@app.route("/")
def start():
    """ Redirect to Home Page """

    return redirect("/users")


@app.route("/users", strict_slashes=False)
def show_users():
    """ 
    Display Home Page: 
    grabs all users from the users table 
    and displays them alphabetically by Last Name
    """

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("user_listing.html", users=users)

################################################################
""" USER ROUTES """

@app.route("/users/new")
def show_new_user_form():
    """ Display new user form"""

    return render_template("user_new.html")


@app.route("/users/new", methods=["POST"])
def process_new_user():
    """ 
    Add new user form contents
    to database as a new User instance
    """

    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url']
    image_url = image_url if image_url else "https://bit.ly/3lUJbon"

    User.create_user(first_name, last_name, image_url)

    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user_details(user_id):
    """ Display detailed page for given user (using user_id)"""

    user = User.query.get_or_404(user_id)
    # print("THIS IS MY USERNAME", user.first_name)

    return render_template("user_detail.html", user=user)


@app.route("/users/<int:user_id>/edit")
def edit_user_details(user_id):
    """ 
    Display user edit form to change user details
    for given user (using user_id)
    """

    user = User.query.get_or_404(user_id)

    return render_template("user_edit.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def process_edit_user(user_id):
    """ 
    Process edit form data and update
    User instance in database
    """
    user = User.query.get_or_404(user_id)

    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["image-url"]
    image_url = image_url if image_url else "https://bit.ly/3lUJbon"

    user.update_user(first_name, last_name, image_url)

    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def process_delete_user(user_id):
    """ Delete given user from database"""
    user = User.query.get_or_404(user_id)

    user.delete_user(user)

    return redirect("/users")


################################################################
""" POSTS ROUTES """

@app.route("/users/<int:user_id>/posts/new")
def show_new_post_form(user_id):
    """ Display new post form for given user"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.order_by(Tag.name).all()

    return render_template("post_new.html", user=user, tags=tags)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def process_post_form(user_id):
    """ 
    Process new post form and create
    Post instance, adding new post to the database
    """

    title = request.form['title']
    content = request.form['content']

    new_post = Post.create_post(title, content, user_id)

    print("TAGS", request.form.getlist("tags"))
    
    for tag_id in request.form.getlist("tags"):
        PostTag.create_posttag(new_post.id, tag_id)
        

    return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>")
def show_post_details(post_id):
    """ Display given post details """

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.order_by(Tag.name).all()

    return render_template("post_detail.html", post=post, tags=tags)

@app.route("/posts/<int:post_id>/edit")
def show_edit_post(post_id):
    """ Display form to edit given post """

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.order_by(Tag.name).all()

    return render_template("post_edit.html", post=post, tags=tags)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def process_edit_post_form(post_id):
    """ 
    Process post edit form and update
    post in database
    """

    post = Post.query.get_or_404(post_id)

    title = request.form['title']
    content = request.form['content']

    post.edit_post(title, content)

    return redirect(f"/posts/{post_id}")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def process_delete_post(post_id):
    """ Delete given post from database """

    post = Post.query.get_or_404(post_id)

    Post.delete_post(post)

    return redirect(f"/users/{post.user_id}")

################################################################
""" TAGS ROUTES """

@app.route("/tags")
def show_tag_list():
    """ Display all tags in the tag table """
    tags = Tag.query.order_by(Tag.name).all()


    return render_template("tag_listing.html", tags=tags)


@app.route("/tags/<int:tag_id>")
def show_tag_details(tag_id):
    """ Display detail page for given tag """

    tag = Tag.query.get_or_404(tag_id)

    posts = tag.posts

    return render_template("tag_detail.html", tag=tag, posts=posts)


@app.route("/tags/new")
def show_new_tag_form():
    """ Display form to add a new tag """

    return render_template("tag_new.html")


@app.route("/tags/new", methods=["POST"])
def process_new_tag_form():
    """ Process new tag form and add tag to database """
    
    name = request.form['name']

    Tag.create_tag(name)
    
    return redirect("/tags")


@app.route("/tags/<int:tag_id>/edit")
def show_edit_form(tag_id):
    
    tag = Tag.query.get_or_404(tag_id)

    return render_template("tag_edit.html", tag=tag)



@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def process_edit_tag_form(tag_id):
    """ Process edit tag form and update database """

    tag = Tag.query.get_or_404(tag_id)
    name = request.form['name']

    tag.update_tag(name)

    return redirect("/tags")


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def process_delete_tag(tag_id):
    """ Deletes tag from database """

    tag = Tag.query.get_or_404(tag_id)

    Tag.delete_tag(tag)

    return redirect("/tags")
