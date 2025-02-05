from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from pathsixgames.config import Config

app = Flask(__name__)

# Load config from Config class
app.config.from_object(Config)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
mail = Mail(app)

from pathsixgames.users.routes import users
from pathsixgames.posts.routes import posts
from pathsixgames.winterMain.routes import winterMain

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(winterMain)