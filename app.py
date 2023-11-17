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

# Declare db tables
userSkillWorkflow = db.Table('UserSkillWorkflow',
    db.Column('skillworkflow_id', db.Integer, db.ForeignKey('SkillWorkflow.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('User.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = "User"

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
    
    education = db.relationship('UserEducation', backref='User', lazy=True)
    experience = db.relationship('UserExperience', backref='User', lazy=True)
    skillworkflow = db.relationship('SkillWorkflow', secondary=userSkillWorkflow, lazy='subquery', backref=db.backref('User', lazy=True))

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

class UserEducation(db.Model):
    __tablename__ = 'UserEducation'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    institution = db.Column(db.String(256), nullable=False)
    facility = db.Column(db.String(256), nullable=False)
    module = db.Column(db.String(256), nullable=False)
    study_period = db.Column(db.String(256), nullable=False)

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return f'<Institution {self.institution}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()

class UserExperience(db.Model):
    __tablename__ = 'UserExperience'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    position = db.Column(db.String(256), nullable=False)
    organization = db.Column(db.String(256), nullable=False)
    work_period = db.Column(db.String(256), nullable=False)

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return f'<Position {self.position}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()

class SkillWorkflow(db.Model):
    __tablename__ = 'SkillWorkflow'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, nullable=False)
    # skill = True, workflow = False
    isSkill = db.Column(db.Boolean, unique=False, default=True)

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    def __init__(self, **kwargs):
        super(SkillWorkflow, self).__init__(**kwargs)

    def __repr__(self):
        return f'<Skill/Workflow {self.name}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()