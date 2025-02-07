from flask import Blueprint

jade = Blueprint('jade', __name__, template_folder='templates', static_folder='static')

from pathsixgames.jade import routes