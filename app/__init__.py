from flask import Flask

# Import Blueprints
from . import database
from . import account
from . import main
from . import quiz


# Setup Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = "x=-p/2+sqrt((p/2)^2-q)"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///App.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BCRYPT_HANDLE_LONG_PASSWORDS'] = True
app.config['CSRF_ENABLED'] = True

# Register Blueprints
app.register_blueprint(account.blueprint)
app.register_blueprint(main.blueprint)
app.register_blueprint(quiz.blueprint)

# Init Database, Bcrypt and Csrf
database.db.init_app(app)
database.bcrypt.init_app(app)
account.csrf.init_app(app)

# Create Database with context
with app.app_context():
    database.db.create_all()
