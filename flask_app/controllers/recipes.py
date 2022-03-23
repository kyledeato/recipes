from crypt import methods
import imp
from flask import render_template, session, redirect, request, flash
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User

@app.route('/dashboard')
def dashboard():
    # protects from typing /dashboard on url
    if not 'user_id' in session:
        return redirect('/')
    recipes = Recipe.get_all()
    #get name for dashboard
    logged_in_user = User.get_by_id({"id": session['user_id']})
    return render_template('dashboard.html', recipes = recipes, user = logged_in_user)

@app.route('/recipes/new')
def new_recipe():
    if not 'user_id' in session:
        return redirect('/')
    return render_template('new_recipe.html')

@app.route('/recipes/<int:id>')
def view_recipe(id):
    if not 'user_id' in session:
        return redirect('/')
    recipe = Recipe.get_one({"id": id})
    return render_template('show_recipe.html', recipe = recipe)

@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    if not 'user_id' in session:
        return redirect('/')
    recipes = Recipe.get_one({"id": id})
    if session["user_id"] == recipes.id:
        return redirect('/dashboard')
    return render_template('edit.html', recipe = recipes)

@app.route('/recipes/destroy/<int:id>')
def destroy(id):
    print("nope")
    id_dict = {"id": id}
    if not 'user_id' in session:
        return redirect('/')
    recipe = Recipe.get_one(id_dict)
    #fix only if logged in user can delete its own recipe
    if session['user_id'] != recipe.id:
        print("went")
        Recipe.delete(id_dict)
    return redirect('/dashboard')


# ACTION
@app.route('/recipes/new/add', methods=['POST'])
def add_recipe():
    # data = {
    #     "user_id": request.form["user_id"],
    #     "name": request.form["name"],
    #     "description": request.form["description"],
    #     "instructions": request.form["instructions"],
    #     "date_made_on": request.form["date_made_on"],
    #     "under_thirty": request.form["under_thirty"]
    # }
    if not Recipe.is_recipe_valid(request.form):
        return redirect('/recipes/new')
    Recipe.add_recipe(request.form)
    return redirect('/dashboard')

@app.route('/recipes/edit', methods=['POST'])
def update():
    if Recipe.is_recipe_valid(request.form):
        recipe_id = Recipe.update(request.form)
        # return redirect('/dashboard')
        return redirect('/dashboard')
    recipe_id = request.form["id"]
    return redirect(f'/recipe/edit/{recipe_id}')