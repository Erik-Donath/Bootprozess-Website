from flask import Blueprint, render_template, request, session

blueprint = Blueprint('main', __name__)


@blueprint.route('/')
@blueprint.route('/index')
def home():
    username = session.get('username') if session.get('logged_in') else None
    return render_template('index.html', route="index", username=username)


@blueprint.route('/impresum', methods=['GET', 'POST'])
def impresum():
    if request.method == 'POST':
        print(f"Kontakt: '{request.form['firstname']} {request.form['lastname']}': {request.form['subject']}")
    return render_template('impresum.html', route="impresum")


@blueprint.route('/quellen')
def quellen():
    return render_template('quellen.html', route="quellen")


@blueprint.route('/boot/')
@blueprint.route('/boot/generel')
def boot_general():
    return render_template('boot/generel.html', route="boot")


@blueprint.route('/boot/windows')
def boot_windows():
    return render_template('boot/windows.html', route="boot")


@blueprint.route('/boot/linux')
def boot_linux():
    return render_template('boot/linux.html', route="boot")
