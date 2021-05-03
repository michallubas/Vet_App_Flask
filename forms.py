from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange
from wtforms import ValidationError
from authproject.models import User,Puppy
from flask import flash

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords must match')])

    pass_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been already registered')

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in data base')

class AddPuppyForm(FlaskForm):
    name = StringField('Add name', validators=[DataRequired()])
    breed = StringField('Add breed', validators=[DataRequired()])
    age = IntegerField('Add age', validators=[DataRequired(), NumberRange(min=0, max=20, message='Add between 0 20')])
    user_id = IntegerField('Add user id', validators=[DataRequired()])
    submit = SubmitField('Confirm add puppy')

    def check_id_double(self,name, breed, age, user_id):
        if Puppy.query.filter_by(name=name, breed=breed, age=age, user_id=user_id).first():
            flash('Puppy already in data base')
            return True
        else:
            return False

class AddNoteForm(FlaskForm):
    note_text = TextField('Put note', validators=[DataRequired()])
    user_id = IntegerField('Add user id', validators=[DataRequired()])
    submit = SubmitField('Confirm add note')

class UploadFileForm(FlaskForm):
    file_name= StringField('File name', validators=[DataRequired()], _name='file_name')
    file = FileField('Upload file', validators=[DataRequired()])
    submit = SubmitField('Confirm')