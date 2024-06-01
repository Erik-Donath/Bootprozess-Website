from flask import Blueprint, render_template, request
routes = Blueprint('main', __name__)


@routes.route('/')
@routes.route('/index')
def home():
    return render_template('index.html', route="index")


@routes.route('/impresum', methods=['GET', 'POST'])
def impresum():
    if request.method == 'POST':
        print(f"Kontakt: '{request.form['firstname']} {request.form['lastname']}': {request.form['subject']}")
    return render_template('impresum.html', route="impresum")


@routes.route('/quellen')
def quellen():
    return render_template('quellen.html', route="quellen")


@routes.route('/boot/')
@routes.route('/boot/generel')
def boot_general():
    return render_template('boot/generel.html', route="boot")


@routes.route('/boot/windows')
def boot_windows():
    return render_template('boot/windows.html', route="boot")


@routes.route('/boot/linux')
def boot_linux():
    return render_template('boot/linux.html', route="boot")
