from flask import Blueprint

routes = Blueprint('routes', __name__)


@routes.route('/r')
def r():
    return "Hey"