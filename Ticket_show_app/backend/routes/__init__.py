from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_cors import CORS
from flask_uploads import UploadSet, IMAGES, configure_uploads
import redis

cur_dir = path.abspath(path.dirname(__file__))
db = SQLAlchemy()
DB_NAME = 'database.sqlite3'
redis_cli = redis.Redis(host="localhost", port=6379, password="", decode_responses=True)
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'helloworld'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///'+path.join(cur_dir,DB_NAME)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/images'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, (photos,))
def create_app():
    db.init_app(app)
    app.app_context().push()
    from Models import admin_model
    from Models import show_model
    from Models import ticket_model
    from Models import user_model
    from Models import venue_model
    #Create the DB
    
    with app.app_context():
        db.create_all()
        admin_user = user_model.Users.query.filter_by(email='admin@gmail.com').first()
        if not admin_user:
        # If the admin user doesn't exist, create it
            admin_user = user_model.Users(name='admin', email='admin@gmail.com', password='Kushal@0807', admin=True)
            db.session.add(admin_user)
            db.session.commit()
    # register routes
    from .auth import auth_routes
    from .admin import admin_routes
    from .bookings import booking
    from .home import home

    app.register_blueprint(auth_routes, url_prefix = "/auth")
    app.register_blueprint(admin_routes,url_prefix='/admin')
    app.register_blueprint(booking,url_prefix='/booking')
    app.register_blueprint(home,url_prefix='/home')
    return app