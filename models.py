"""Models for Blogly."""

import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """ User Model """

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(50),
                           nullable=False)

    last_name = db.Column(db.String(50),
                          nullable=False)

    image_url = db.Column(db.Text,
                          nullable=True)

    posts = db.relationship('Post')

    def __repr__(self):
        s = self
        return f"<User {s.id} {s.first_name} {s.last_name} {s.image_url}>"

    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"

    @staticmethod
    def create_user(first_name, last_name, image_url):
        new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        db.session.add(new_user)
        db.session.commit()

    def update_user(self, first_name, last_name, image_url):
        self.first_name = first_name
        self.last_name = last_name
        self.image_url = image_url
        db.session.commit()

    def delete_user(self, user):
        db.session.delete(user)
        db.session.commit()


class Post(db.Model):
    """ Blog post model"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.String(50),
                      nullable=False)

    content = db.Column(db.Text)

    created_at = db.Column(db.DateTime,
                           default=datetime.datetime.utcnow())

    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"))

    user = db.relationship('User')

    tags = db.relationship('Tag', secondary='post_tag')

    def __repr__(self):
        s = self
        return f"<Post {s.id} {s.title} {s.content} {s.created_at} {s.user_id}>"

    @staticmethod
    def create_post(title, content, user_id):
        new_post = Post(title=title, content=content, user_id=user_id)
        db.session.add(new_post)
        db.session.commit()

        return new_post
    
    def edit_post(self, title, content):
        self.title = title
        self.content = content
        
        db.session.commit()

    @staticmethod
    def delete_post(post):
        db.session.delete(post)
        db.session.commit()


class Tag(db.Model):
    """ Creates tag """

    __tablename__ = "tags"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    name =   db.Column(db.String(50), unique=True)

    posts = db.relationship('Post', secondary='post_tag')

    @staticmethod
    def create_tag(name):
        new_tag = Tag(name=name)
        db.session.add(new_tag)
        db.session.commit()

    def update_tag(self, name):
        self.name = name
        db.session.commit()

    @staticmethod
    def delete_tag(tag):
        db.session.delete(tag)
        db.session.commit()


class PostTag(db.Model):
    """ Creates the post_tag join table """

    __tablename__ = "post_tag"

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key=True)
    
    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.id'),
                       primary_key=True)

    posts = db.relationship('Post')

    tags = db.relationship('Tag')

    @staticmethod
    def create_posttag(post_id, tag_id):
        new_posttag = PostTag(post_id=post_id, tag_id=tag_id)
        db.session.add(new_posttag)
        db.session.commit()


def example_data():
    """Create some sample data."""

    # In case this is run more than once, empty out existing data
    User.query.delete()

    # Add users
    u1 = User(first_name='Mack',
              last_name='Cooper',
              image_url='https://bit.ly/3462Qfn')
    u2 = User(first_name='Andrew',
              last_name='Dietrich',
              image_url='https://bit.ly/3k4epcb')

    p1 = Post(title='My First Post',
              content='This is great. Yes it is.',
              user_id=1)

    p2 = Post(title='Things I learned about SQAlchemy through the fire',
              content='It began on a caffeinated Wednesday morning...',
              user_id=2)
    
    t1 = Tag(name="Wowza")

    t2 = Tag(name="MustReadNow")

    pt1 = PostTag(post_id=1, tag_id=1)

    pt2 = PostTag(post_id=1, tag_id=2)

    pt3 = PostTag(post_id=2, tag_id=1)

    example_list = [u1, u2, p1, p2, t1, t2, pt1, pt2, pt3]

    db.session.add_all(example_list)
    db.session.commit()


def connect_db(app):
    """Connect the database to our Flask app."""

    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # So that we can use Flask-SQLAlchemy, we'll make a Flask app
    from app import app

    connect_db(app)

    db.drop_all()
    db.create_all()

    example_data()
