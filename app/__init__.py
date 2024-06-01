from flask import Flask

# Import Blueprints
from . import main
from . import quiz

# Setup Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = "x=-p/2+sqrt((p/2)^2-q)"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Register Blueprints
app.register_blueprint(main.routes)
app.register_blueprint(quiz.routes)

# Init Database
quiz.db.init_app(app)
with app.app_context():
    quiz.db.create_all()

