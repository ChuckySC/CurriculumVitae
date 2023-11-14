from flask import Flask, render_template, abort, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import datetime

import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(256), nullable=False)
    lastname = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    bio = db.Column(db.Text)
    li = db.Column(db.String(256), unique=True, nullable=False)
    gh = db.Column(db.String(256), unique=True, nullable=False)
    
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<User {self.firstname}>'

# @app.route('/')
# def home():
#     return f"I'm alive. Move on..."

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)

@app.context_processor
def inject_now():
    return {'current_year': datetime.utcnow().year}

@app.route('/', methods=['GET'])
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        # logger for errors
        abort(500)

@app.route('/<id>', methods=['GET'])
def index_custom(id):
    try:
        user = User.query.get(int(id))
        context = {
            "firstname": user.firstname,
            'lastname': user.lastname,
            'email': user.email,
            'bio': user.bio,
            'linkedin': user.li,
            'github': user.gh
        }
        return render_template('index-custom.html', context=context)
    except Exception as e:
        # logger for errors
        abort(500)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        student = User(
            firstname=request.form['firstname'],
            lastname=request.form['lastname'],
            email=request.form['email'],
            bio=request.form['bio'],
            li=request.form['li'],
            gh=request.form['gh']
        )
        db.session.add(student)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('create.html')