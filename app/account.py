from flask import Blueprint, redirect, url_for, render_template, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import InputRequired, Email, Length
from flask_wtf.csrf import CSRFProtect

from .database import db, Users

blueprint = Blueprint('account', __name__)
csrf = CSRFProtect()


class LoginForm(FlaskForm):
    username = StringField('Nutzername', validators=[InputRequired(), Length(min=3, max=15)])
    password = PasswordField('Passwort', validators=[InputRequired(), Length(min=8)])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Nutzername', validators=[InputRequired(), Length(min=3, max=15)])
    email = EmailField('E-Mail', validators=[InputRequired(), Email(), Length(min=5, max=50)])
    password = PasswordField('Passwort', validators=[InputRequired(), Length(min=8)])
    submit = SubmitField('Registrieren')


@blueprint.route('/account/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('account.view'))
    if request.method != 'POST':
        return render_template('account/login.html', route="account", failed=None, form=LoginForm())

    form = LoginForm()
    if not form.validate_on_submit():
        reasons = []
        for field, errors in form.errors.items():
            if field == "username":
                reasons.append("Der Nutzername muss zwischen 3 und 30 Buchstaben lang sein.")
            elif field == "password":
                reasons.append("Das Passwort muss mindestens 8 Buchstaben lang sein.")
            else:
                reasons.append(f"Anderer Fehler ({', '.join(errors)})")
        return render_template('account/login.html', route="account", failed="validation", reasons=reasons)

    user = Users.query.filter_by(username=form.username.data).first()
    if not user:
        return render_template('account/login.html', route="account", failed="not_exist")

    if not user.check_password(form.password.data):
        return render_template('account/login.html', route="account", failed="wrong_password")

    session['logged_in'] = True
    session['id'] = user.id
    session['username'] = user.username
    session['email'] = user.email

    return redirect(url_for('account.view'))


@blueprint.route('/account/register', methods=['GET', 'POST'])
def register():
    if session.get('logged_in'):
        return redirect(url_for('account.view'))

    if request.method != 'POST':
        return render_template('account/register.html', route="account", failed=None, form=RegisterForm())

    form = RegisterForm()
    if not form.validate_on_submit():
        reasons = []
        for field, errors in form.errors.items():
            if field == "username":
                reasons.append("Der Nutzername muss zwischen 3 und 30 Buchstaben lang sein.")
            elif field == "email":
                reasons.append("Die E-Mail muss zwischen 5 und 50 Buchstaben lang sein und valide sein.")
            elif field == "password":
                reasons.append("Das Passwort muss mindestens 8 Buchstaben lang sein.")
            else:
                reasons.append(f"Anderer Fehler ({', '.join(errors)})")
        return render_template('account/register.html', route="account", failed="validation", reasons=reasons)

    if (Users.query.filter_by(username=form.username.data).first()
            or Users.query.filter_by(email=form.email.data).first()):
        return render_template('account/register.html', route="account", failed="already_exist")

    user = Users(username=form.username.data, email=form.email.data, password=form.password.data)
    db.session.add(user)
    db.session.commit()

    session['logged_in'] = True
    session['id'] = user.id
    session['username'] = user.username
    session['email'] = user.email

    return redirect(url_for('account.view'))


@blueprint.route('/account/logout', methods=['GET', 'POST'])
def logout():
    session.pop('logged_in', False)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('email', None)

    return render_template('account/logout.html', route="account")


@blueprint.route('/account/delete', methods=['GET', 'POST'])
def delete():
    if not session.get('logged_in'):
        return redirect(url_for('account.login'))

    Users.query.filter_by(id=session['id']).delete()
    db.session.commit()

    session.pop('id', None)
    return redirect(url_for('account.logout'))


@blueprint.route('/account/view', methods=['GET', 'POST'])
def view():
    if not session.get('logged_in'):
        return redirect(url_for('account.login'))

    user = Users.query.filter_by(id=session.get('id')).first()
    if not user:
        return redirect(url_for('account.logout'))

    return render_template('account/view.html', route="account", user=user)
