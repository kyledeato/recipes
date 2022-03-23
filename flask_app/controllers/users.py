from flask import render_template, session, redirect, request, flash
from flask_app import app
from flask_app.models.user import User

# DISPLAY
@app.route('/')
def index():
    # logs you out when typing /
    if 'user_id' in session:
        return redirect('/logout')
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')





# ACTION
@app.route('/register',methods=['POST'])
def register():
    if request.form['forms'] == 'register':
        if User.reg_is_valid(request.form):
            session['user_id'] = User.create(request.form)
            return redirect('/dashboard')
        else:
            print("invalid")
            return redirect('/')

    if request.form['forms'] == 'login':
        data = {
            "email": request.form["email"],
            "password": request.form["password"]
        }
        if not User.log_valid(data):
           flash("invalid login")
           return redirect('/')

        user = User.get_by_email(data)
        session['user_id'] = user.id
        return redirect('/dashboard')