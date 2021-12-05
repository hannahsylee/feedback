from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import UserForm, LoginForm, FeedbackForm, DeleteForm
from werkzeug.exceptions import Unauthorized
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "flaskfeedback"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)

toolbar = DebugToolbarExtension(app)

@app.route('/')
def home_page():

    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Show a form that when submitted will register/create a user."""
    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = UserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken. Please pick another')
            return render_template('register.html', form=form)
        session['username'] = new_user.username
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect(f'/users/{new_user.username}')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Show a form that when submitted will login a user."""
    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!", "primary")
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username/password.']
            return render_template('login.html', form=form)

    return render_template('login.html', form=form)

@app.route('/users/<username>')
def user(username):
    """Display a template the shows information about that user"""
    # if "username" not in session or username != session['username']:
    #     raise Unauthorized()
    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    form = DeleteForm()

    return render_template('users/user.html', user=user, form=form)

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    """Remove the user from the database and make sure to also delete all of their feedback."""
    if "username" not in session or username != session['username']:
        raise Unauthorized()
        
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop('username')

    return redirect('/')

@app.route('/users/<username>/feedback/add', methods=['GET','POST'])
def add_feedback(username):
    """Display a form to add feedback"""
    if "username" not in session or username != session['username']:
        raise Unauthorized()

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_feedback = Feedback(title=title, content=content, username=username)
        db.session.add(new_feedback)
        db.session.commit()

        return redirect(f'/users/{new_feedback.username}')
    else:
        return render_template('feedback/add.html', form=form)

@app.route('/feedback/<int:id>/update', methods=['GET','POST'])
def update_feedback(id):
    """Display a form to edit feedback"""
    feedback = Feedback.query.get(id)

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f'/users/{feedback.username}')
    else:
        return render_template('feedback/edit.html', form=form)

@app.route('/feedback/<int:id>/delete', methods=['POST'])
def delete_feedback(id):
    """Delete a specific piece of feedback"""
    feedback = Feedback.query.get(id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f'/users/{feedback.username}')

@app.route('/logout')
def logout():
    """Clear any information from the session and redirect to /"""
    session.pop('username')
    flash("Goodbye!", "info")
    return redirect('/')




