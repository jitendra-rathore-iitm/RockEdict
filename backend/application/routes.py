from .main import api, db, bcrypt
from .models import User
from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required



class Register(Resource):
    def post(self):
        name = request.json.get("name")
        email = request.json.get("email")
        password = request.json.get("password")
        if not name or not email or not password:
            return {"message": "All fields are required"}, 400
        email = email.lower()
        existing_user = db.session.execute(db.select(User).filter_by(email = email)).scalar_one_or_none()
        if existing_user:
            return {"message": f"{name}, you have already an account. please login"}, 400
        db.session.add(User(name = name, email = email, password = bcrypt.generate_password_hash(password).decode("utf-8")))
        db.session.commit()
        return {"message": f"{name}, your account is created successfully"}, 201

class Login(Resource):
    def post(self):
        email = request.json.get("email")
        password = request.json.get("password")
        if not email or not password:
            return {"message": "All fields are required"}, 400
        email = email.lower()
        user = db.session.execute(db.select(User).filter_by(email = email)).scalar_one_or_none()
        if user and bcrypt.check_password_hash(user.password, password) :
            access_token = create_access_token(identity=user.email)
            return {"access_token": access_token}, 200
        return {"message": "Invalid credentials"}, 401



class HelloWorld(Resource):
    def get(self):
        return {"message": "Hello World"}

api.add_resource(HelloWorld, "/")
api.add_resource(Register, "/api/register")
api.add_resource(Login, "/api/login")
