from authproject import app, db, UPLOAD_FOLDER
from flask import redirect, url_for, render_template, flash, abort, request
from flask_login import login_user, login_required, logout_user
from authproject.models import User, Puppy, Note, File
from authproject.forms import LoginForm, RegistrationForm, AddPuppyForm, AddNoteForm, UploadFileForm
import os
from werkzeug.utils import secure_filename
import copy

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out')
    return redirect(url_for('home'))

@app.route('/login', methods = ['POST', 'GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:

            login_user(user)
            flash('Logged in Successfully')
            flash(f'Your puppies: {user.puppies}')

            next = request.args.get('next')

            if next is None or not next[0]=='/':
                next = url_for('welcome_user')

            return redirect(next)
        else:
            flash(f'Bad password, try again user: {form.email.data}')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route('/register', methods= ['POST', 'GET'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registration')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)



@app.route('/addPuppy', methods= ['POST', 'GET'])
@login_required
def add_puppy():
    form = AddPuppyForm()

    if form.validate_on_submit():
        name = form.name.data
        breed = form.breed.data
        age = form.age.data
        user_id = form.user_id.data

        if form.check_id_double(name,breed,age,user_id):
            flash(f'Puppy {name} already in database')
            return redirect(url_for('home'))
        else:


            newPuppy = Puppy(name,breed,age,user_id)

            db.session.add(newPuppy)
            db.session.commit()

            temp_user = User.query.filter_by(id=user_id).first()

            flash(f'Added pupy {name}, age: {age}')
            flash(f'Your puppies: {temp_user.puppies}')

            return redirect(url_for('home'))


    return render_template('add_puppy.html', form = form)


@app.route('/addNote', methods= ['POST', 'GET'])
@login_required
def add_note():
    form = AddNoteForm()

    if form.validate_on_submit():
        note_text = form.note_text.data
        user_id = form.user_id.data

        newNote = Note(note_text,user_id)

        db.session.add(newNote)
        db.session.commit()

        return redirect(url_for('home'))


    return render_template('add_note.html', form = form)


@app.route('/all_puppies', methods=['POST', 'GET'])
def all_puppies():
    list_puppies = Puppy.query.all()

    return render_template('list_puppies.html', list_puppies=list_puppies)

@app.route('/all_users', methods=['POST', 'GET'])
def all_users():
    list_users = User.query.all()

    return render_template('list_users.html', list_users=list_users)

@app.route('/all_notes', methods=['POST', 'GET'])
def all_notes():
    list_notes = Note.query.all()

    return render_template('list_notes.html', list_notes=list_notes)

@app.route('/add_file', methods=['POST', 'GET'])
def add_file():
    form = UploadFileForm()

    if form.validate_on_submit():
        file = request.files['file']

        #to db
        newFile = File(form.file_name.data,file.read())


        #to folder
        #first put cursor at the begining of file
        file.seek(0)
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))





        print(type(file))

        # file.close()

        db.session.add(newFile)
        db.session.commit()

    return render_template('add_file.html', form=form)

@app.route('/all_files', methods=['POST', 'GET'])
def all_files():
    list_files = File.query.all()

    return render_template('list_files.html', list_files=list_files)

if __name__ == "__main__":
    app.run(debug=True)