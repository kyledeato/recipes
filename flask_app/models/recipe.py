import queue
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models import user

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_thirty = data['under_thirty']
        self.date_made_on = data['date_made_on']

    @classmethod
    def add_recipe(cls, data):
        query = 'INSERT INTO recipes (name,description, instructions, under_thirty, date_made_on, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(under_thirty)s, %(date_made_on)s, %(user_id)s);'
        return connectToMySQL('recipes').query_db(query, data)
        
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;"
        results = connectToMySQL('recipes').query_db(query)
        recipes = []
        if results:
            for row in results:
                #makes a temp row with creator
                temp_recipes = cls(row)
                user_data = {
                    "id": row["users.id"],
                    "first_name": row["first_name"],
                    "last_name": row["last_name"],
                    "email": row["email"],
                    "password": row["password"],
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"],
                }
                #making a "creator" field in the row and pass through User instance
                temp_recipes.creator = user.User(user_data)
                recipes.append(temp_recipes)
            return recipes
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;"
        results = connectToMySQL('recipes').query_db(query, data)
        if results:
            temp_recipe = cls(results[0])
            temp_recipe.creator = user.User(results[0])
            
            return temp_recipe

    @classmethod
    def update(cls, data):
        query = 'UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, under_thirty = %(under_thirty)s, date_made_on = %(date_made_on)s'
        connectToMySQL('recipes').query_db(query, data)
        return data["id"]
    
    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM recipes WHERE id = %(id)s'
        connectToMySQL('recipes').query_db(query, data)

    @staticmethod
    def is_recipe_valid(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            flash("Name must be at least 3 characters long.")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("Descriptions must be at least 3 characters long.")
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("Instructions must be at least 3 characters long.")
            is_valid = False
        if recipe['date_made_on'] == "":
            flash("Enter a date")
            is_valid = False
       
        return is_valid
