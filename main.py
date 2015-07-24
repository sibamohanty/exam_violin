from flask import Flask
from flask.ext.sqlalchemy import  SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/tutor'
db = SQLAlchemy(app)

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app

class User(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    username = db.Column(db.String(80), unique= True)
    email = db.Column(db.String(120), unique=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    organization = db.relationship('Organization',
        backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, username,email,organization):
        self.username = username
        self.email = email
        self.organization = organization

    def __repr__(self):
        return '<User %r>' % self.username

class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))


class Group(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    group_name = db.Column(db.String(100), unique = True)
    group_mail = db.Column(db.String(100), unique = True)

class Questions(db.Model):

    id= db.Column(db.Integer, primary_key = True)
    TYPES = [
        "mcma",
        "mcsa",
        "tf"
    ]
    question = db.Column(db.Text)
    q_type = db.Column(db.Enum(*TYPES,name="q_types"))
    #answer = db.Column(db.String(20))

    def __init__(self,question,q_type):
        self.question = question
        self.q_type = q_type

class CorrectAnswer(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    question_id =  db.Column(db.Integer,db.ForeignKey(Questions.id))
    answer_key = db.Column(db.Text)

class Answers(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    question_id =  db.Column(db.Integer,db.ForeignKey(Questions.id))
    answer = db.Column(db.Text)
    correct = db.Column(db.Boolean)
    question = db.relationship(Questions)
    def __init__(self,answer, correct, question):
        self.answer = answer
        self.correct = correct
        self.question = question

    def __repr__(self):
        return '<Answer %r>' % self.answer
