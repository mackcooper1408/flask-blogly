"""Models for Blogly."""
from sqlalchemy import 

class User(db.Model):
    """ User Model """

    __tablename__ = "user"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column()