"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """ User Model """

    __tablename__ = "user"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                           nullable=False)
    last_name = db.Column(db.String(50),
                          nullable=False)
    image_url = db.Column(db.Text,
                          nullable=True,
                          default='https://immedilet-invest.com/wp-content/uploads/2016/01/user-placeholder.jpg')

    def __repr__(self):
        s = self
        return f"User {s.id} {s.first_name} {s.last_name} {s.image_url}"
