from flask import Flask
from database import Firebase
from .views import views
from .auth import auth
from .models import User,Note
#from flask_login import LoginManager

db = Firebase()



def create_app():
    app = Flask(__name__)
    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    return app
    #@login_manager.user_loader


def load_user():
    return db.get_users()

def load_note():
    return db.get_notes()







