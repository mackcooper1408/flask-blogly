"""Models for Blogly."""

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

    def __repr__(self):
        s = self
        return f"User {s.id} {s.first_name} {s.last_name} {s.image_url}"

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


def example_data():
    """Create some sample data."""

    # In case this is run more than once, empty out existing data
    User.query.delete()

    # Add users
    u1 = User(first_name='Mack',
              last_name='Cooper',
              image_url='https://images.pexels.com/photos/771742/pexels-photo-771742.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500')
    u2 = User(first_name='Andrew',
              last_name='Dietrich',
              image_url='https://www.postplanner.com/hs-fs/hub/513577/file-2886416984-png/blog-files/facebook-profile-pic-vs-cover-photo-sq.png?width=250&height=250&name=facebook-profile-pic-vs-cover-photo-sq.png')

    db.session.add_all([u1, u2])
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
