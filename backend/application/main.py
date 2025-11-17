from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_bcrypt import Bcrypt
from flask_restful import Api
from flask_jwt_extended import JWTManager

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chat_db.sqlite3"
app.config["JWT_SECRET_KEY"] = "super-secret-key"  
jwt = JWTManager(app)
api = Api(app)


db.init_app(app)
bcrypt = Bcrypt(app)
from .models import User
with app.app_context():
    db.create_all()
    email = "jitendra@rockedict.in"
    existing_user = db.session.execute(db.select(User).filter_by(email = email)).scalar_one_or_none()
    if not existing_user:
        db.session.add(User(name = "Jitendra", email = email, password = bcrypt.generate_password_hash("Jitendra123").decode("utf-8"), role = "Admin"))
        db.session.commit()

from . import routes

