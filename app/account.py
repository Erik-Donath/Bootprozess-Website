from flask import Blueprint, redirect, url_for, render_template, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
from flask_wtf.csrf import CSRFProtect

from .user import Profile

blueprint = Blueprint('account', __name__)
csrf = CSRFProtect()


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=3, max=15)])
    password = PasswordField(validators=[InputRequired(), Length(min=8)])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=3, max=15)])
    password = PasswordField(validators=[InputRequired(), Length(min=8)])
    submit = SubmitField('Registrieren')


@blueprint.route('/account/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('account.view'))
    if request.method != 'POST':
        return render_template('account/login.html', route="account", failed=None, form=LoginForm(), profile=Profile.getProfile())

    form = LoginForm()
    if not form.validate_on_submit():
        reasons = genReasons(form.errors)
        return render_template('account/login.html', route="account", failed="validation", reasons=reasons, profile=Profile.getProfile())

    res = Profile.login(form.username.data, form.password.data)
    if res == 1:
        return render_template('account/login.html', route="account", failed="not_exist", profile=Profile.getProfile())
    if res == 2:
        return render_template('account/login.html', route="account", failed="wrong_password", profile=Profile.getProfile())

    return redirect(url_for('account.view'))


@blueprint.route('/account/register', methods=['GET', 'POST'])
def register():
    if session.get('logged_in'):
        return redirect(url_for('account.view'))

    if request.method != 'POST':
        return render_template('account/register.html', route="account", failed=None, form=RegisterForm(), profile=Profile.getProfile())

    form = RegisterForm()
    if not form.validate_on_submit():
        reasons = genReasons(form.errors)
        return render_template('account/register.html', route="account", failed="validation", reasons=reasons, profile=Profile.getProfile())

    res = Profile.register(form.username.data, form.password.data)
    if res == 1:
        return redirect(url_for('account.view'))
    if res == 2:
        return render_template('account/register.html', route="account", failed="already_exist", profile=Profile.getProfile())

    return redirect(url_for('account.view'))


@blueprint.route('/account/logout', methods=['GET', 'POST'])
def logout():
    Profile.logout()
    return render_template('account/logout.html', route="account", profile=Profile.getProfile())


@blueprint.route('/account/delete', methods=['GET', 'POST'])
def delete():
    res = Profile.delete()
    if res == 1:
        return redirect(url_for('account.login'))
    return redirect(url_for('account.logout'))


@blueprint.route('/account/view', methods=['GET', 'POST'])
def view():
    if not session.get('logged_in'):
        return redirect(url_for('account.login'))

    return render_template('account/view.html', route="account", profile=Profile.getProfile())


@blueprint.route('/account/set/icon/<icon>', methods=['GET', 'POST'])
def updateIcon(icon: int):
    res = Profile.updateIcon(icon)

    if res == 1:
        return redirect(url_for('account.login'))
    if res == 2:
        return redirect(url_for('account.register'))
    return redirect(url_for('account.view', _anchor="icon"))


def genReasons(errors):
    reasons = []
    for field, errors in errors.items():
        if field == "username":
            reasons.append("Der Nutzername muss zwischen 3 und 30 Buchstaben lang sein.")
        elif field == "password":
            reasons.append("Das Passwort muss mindestens 8 Buchstaben lang sein.")
        else:
            reasons.append(f"Anderer Fehler ({', '.join(errors)})")
    return reasons
