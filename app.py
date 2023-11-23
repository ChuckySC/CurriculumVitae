from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, update, delete, values
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

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)

# Declare db tables
class User(db.Model):
    __tablename__ = 'User'

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

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return f'<User {self.firstname}>'

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.id
        except Exception as e:
            # logger for errors
            db.session.close()

    def remove(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            # logger for errors
            db.session.close()

class Skill(db.Model):
    __tablename__ = 'Skill'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, nullable=False)
    # skill = True, workflow = False
    is_skill = db.Column(db.Boolean, unique=False, default=True)

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    def __init__(self, **kwargs):
        super(Skill, self).__init__(**kwargs)

    def __repr__(self):
        return f'<Skill {self.name}>'

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            # logger for errors
            db.session.close()

    def remove(self):
        try:
            if db.session.query(UserSkill.skill_id).filter_by(id=self.id).first() is None:
                # delete if skill is not linked to any user
                db.session.delete(self)
                db.session.commit()
            # else:
                # TODO trigger notification msg pop up
        except Exception as e:
            # logger for errors
            db.session.close()

class UserEducation(db.Model):
    __tablename__ = 'UserEducation'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    institution = db.Column(db.String(256), unique=False, nullable=False)
    facility = db.Column(db.String(256), unique=False, nullable=False)
    module = db.Column(db.String(256), unique=False, nullable=False)
    study_period = db.Column(db.String(256), unique=False, nullable=False)
    # education=True, course=False
    is_education = db.Column(db.Boolean, unique=False, default=True)

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    def __init__(self, **kwargs):
        super(UserEducation, self).__init__(**kwargs)

    def __repr__(self):
        return f'<Institution {self.institution}>'

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            # logger for errors
            db.session.close()

    def remove(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            # logger for errors
            db.session.close()

    def removeAll(id):
        try:
            sql = delete(UserEducation).where(UserEducation.user_id == id)

            db.session.execute(sql)
            db.session.commit()
        except Exception as e:
            # logger for errors
            db.session.close()

class UserExperience(db.Model):
    __tablename__ = 'UserExperience'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    position = db.Column(db.String(256), unique=False, nullable=False)
    organization = db.Column(db.String(256), unique=False, nullable=False)
    work_period = db.Column(db.String(256), unique=False, nullable=False)

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    def __init__(self, **kwargs):
        super(UserExperience, self).__init__(**kwargs)

    def __repr__(self):
        return f'<Position {self.position}>'

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            # logger for errors
            db.session.close()

    def remove(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            # logger for errors
            db.session.close()

    def removeAll(id):
        try:
            sql = delete(UserExperience).where(UserExperience.user_id == id)

            db.session.execute(sql)
            db.session.commit()
        except Exception as e:
            # logger for errors
            db.session.close()

class UserSkill(db.Model):
    __tablename__ = 'UserSkill'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=False, nullable=False)
    skill_id = db.Column(db.Integer, unique=False, nullable=False)
    
    def __init__(self, **kwargs):
        super(UserSkill, self).__init__(**kwargs)
    
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            # logger for errors
            db.session.close()

    def remove(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            # logger for errors
            db.session.close()
    
    def removeAll(id):
        try:
            # sql = delete(UserSkill).where(UserSkill.user_id.in_([ids]))
            sql = delete(UserSkill).where(UserSkill.user_id == id)

            db.session.execute(sql)
            db.session.commit()
        except Exception as e:
            # logger for errors
            db.session.close()