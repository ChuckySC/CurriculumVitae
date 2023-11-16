from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask import Flask
import os

from app_views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)

# Set up the database connection
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)

# Declare the db table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(256), nullable=False)
    lastname = db.Column(db.String(256), nullable=False)
    street = db.Column(db.String(256), nullable=False)
    city = db.Column(db.String(256), nullable=False)
    postcode = db.Column(db.String(256), nullable=False)
    phone = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    bio = db.Column(db.Text)
    li = db.Column(db.String(256), unique=True, nullable=False)
    gh = db.Column(db.String(256), unique=True, nullable=False)

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return f'<User {self.firstname}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()