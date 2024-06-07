from flask import Blueprint, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length

from .database import db, Contacts
from .user import Profile

blueprint = Blueprint('main', __name__)


class KontaktForm(FlaskForm):
    firstname = StringField(validators=[InputRequired(), Length(max=15)])
    lastname = StringField(validators=[InputRequired(), Length(max=15)])
    subject = StringField(validators=[InputRequired(), Length(min=10, max=500)])
    submit = SubmitField("Absenden")


@blueprint.route('/')
@blueprint.route('/index')
def home():
    return render_template('index.html', route="index", profile=Profile.getProfile())


@blueprint.route('/impresum', methods=['GET', 'POST'])
def impresum():
    if request.method == 'POST':
        form = KontaktForm()
        if not form.validate_on_submit():
            return redirect(url_for('main.impresum', _anchor="kontakt"))
        contact = Contacts(form.firstname.data, form.lastname.data, form.subject.data)
        db.session.add(contact)
        db.session.commit()

        print(f"Stored Contact: '{request.form['firstname']} {request.form['lastname']}': {request.form['subject']}")
    return render_template('impresum.html', route="impresum", profile=Profile.getProfile(), form=KontaktForm())


@blueprint.route('/quellen')
def quellen():
    return render_template('quellen.html', route="quellen", profile=Profile.getProfile())


@blueprint.route('/boot/')
@blueprint.route('/boot/windows')
def boot_windows():
    return render_template('boot/windows.html', route="boot", profile=Profile.getProfile())


@blueprint.route('/boot/linux')
def boot_linux():
    return render_template('boot/linux.html', route="boot", profile=Profile.getProfile())


@blueprint.route('/boot/macos')
def boot_general():
    return render_template('boot/macos.html', route="boot", profile=Profile.getProfile())