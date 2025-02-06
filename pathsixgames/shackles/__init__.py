from flask import Blueprint

shackles = Blueprint('shackles', __name__, template_folder='templates', static_folder='static')

from pathsixgames.shackles import routes
