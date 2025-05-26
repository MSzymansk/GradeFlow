from functools import wraps
from flask import session, redirect, url_for, flash, render_template, Blueprint
from flask.cli import with_appcontext
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms.fields.simple import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from application.database.models import Teacher
from application.extensions import db

auth_bp = Blueprint('auth', __name__)

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    submit = SubmitField('Zaloguj się')

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'teacher_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return wrapper

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        teacher = Teacher.query.filter(Teacher.email == form.email.data).first()
        if teacher and check_password_hash(teacher.password_hash, form.password.data):
            session['teacher_id'] = teacher.id
            flash('Zalogowano pomyślnie')
            return redirect(url_for('dashboard.dashboard'))
        flash('Błędny email lub hasło')
    return render_template('login.html', form=form)


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Wylogowano pomyślnie')
    return redirect(url_for('auth.login'))


@auth_bp.cli.command('create-teacher')
@with_appcontext
def create_teacher():
    name = input("Podaj imię: ")
    surname = input("Podaj nazwisko: ")
    pesel = input("Podaj PESEL: ")
    email = input("Podaj email: ")
    password = input("Podaj hasło: ")

    try:
        hashed = generate_password_hash(password)
        t = Teacher(
            name=name,
            surname=surname,
            pesel=int(pesel),
            email=email,
            password_hash=hashed
        )
        db.session.add(t)
        db.session.commit()
        print("Nauczyciel utworzony! ID:", t.id)
    except Exception as e:
        db.session.rollback()
        print(" Błąd:", e)