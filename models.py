from authproject import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True,
                      index=True)
    username = db.Column(db.String(64), unique=True,
                         index=True )
    password_hash = db.Column(db.String(128))
    puppies= db.relationship('Puppy', backref='user')
    notes=db.relationship('Note', backref='user')

    def __repr__(self):
        return f'User {self.username}, email: {self.email}, id: {self.id}, puppies: {self.puppies} '


    def __init__(self, email, username, password):
        self.email=email
        self.username=username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Puppy(db.Model):
    __tablename__ = 'puppies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24))
    breed = db.Column(db.String(24))
    age = db.Column(db.Integer)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id') )

    def __init__(self, name, breed,age, user_id):
        self.name = name
        self.breed = breed
        self.age = age
        self.user_id=user_id

    # def check_if_double(self, name, breed, age, user_id):
    #     check= self.name == name and self.breed == breed
    #            # and self.breed == breed and self.age == age and self.user_id ==user_id
    #     print(check)
    #     return check

    def __repr__(self):
        return f'Pet {self.name}, breed: {self.breed}, age: {self.age}, id: {self.id}'

class Note(db.Model):
    __tablename__ = 'notes'

    id=db.Column(db.Integer, primary_key=True)
    note_text=db.Column(db.Text, nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'))
    date_created=db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, note_text, user_id):
        self.note_text=note_text
        self.user_id=user_id

    def __repr__(self):
        return f'Note from: {self.date_created}, starts with: {self.note_text[:8]}'

class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    file = db.Column(db.LargeBinary)

    def __init__(self, name, file):
        self.name=name
        self.file=file

    def __repr__(self):
        return f'File: {self.name}, {self.file}'