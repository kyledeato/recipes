from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    
    @classmethod
    def create(cls, data):
        pw_hash = bcrypt.generate_password_hash(data['password'])
        hashed_dict ={
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "email": data["email"],
            "password": pw_hash
        }

        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL('recipes').query_db(query, hashed_dict)

    @classmethod
    def get_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s'
        result = connectToMySQL('recipes').query_db(query, data)
        if result:
            return cls(result[0])
    
    @classmethod
    def get_by_id(cls, data):
        query = 'SELECT * FROM users WHERE id = %(id)s'
        result = connectToMySQL('recipes').query_db(query, data)
        if result:
            return cls(result[0])

    @staticmethod
    def reg_is_valid(user):
        is_valid = True
        query = 'SELECT * FROM users WHERE email = %(email)s'
        results = connectToMySQL('recipes').query_db(query, user)
        if EMAIL_REGEX.match(user['email']):
            is_valid = True
        else:
            flash("Invalid email address")
            is_valid = False
        if len(results) >= 1:
            flash("Email already taken")
            is_valid = False
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.")
            is_valid = False
        if len(user['last_name']) < 2: # need regex for names not only letters
            flash("Last name must be at least 2 characters.")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        if user['password'] != user['confirm_password']:
            is_valid = False
            flash("Password does not match")

        return is_valid
    
    @staticmethod
    def log_valid(data):
        user = User.get_by_email(data)

        if not user:
            return False
        
        if not bcrypt.check_password_hash(user.password, data["password"]):
            return False

        return True
        
        