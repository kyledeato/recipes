from flask import render_template, session, redirect, request
from flask_app import app
from flask_app.models.user import User


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['POST'])
def register():
    if request.form['forms'] == 'register':
        if User.reg_is_valid(request.form):
            User.create(request.form)
            return redirect('/')
        else:
            print("invalid")
            return redirect('/')
    if request.form['forms'] == 'login':
        pass