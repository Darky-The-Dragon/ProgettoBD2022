from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# The URL that our website has

# Define of blueprint
auth = Blueprint('auth', __name__)


# To get the information from the HTML page we need to say if the page accepts data methods=['GET', 'POST']
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            elif len(password) == 0:
                flash('Password field can\'t be empty.', category='error')
            elif len(password) < 6:
                flash('Password must be at least 6 characters.', category='error')
            else:
                flash('Incorrect password, try again.', category='error')
        elif len(email) == 0:
            flash('Email field can\'t be empty.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        else:
            flash('Email does not exist.', category='error')

        # To get and access to the information we got from the form we need to:
    # data = request.form
    # I can print the data i received with
    # print(data)
    # I can pass variables followed by a ",". Examples: text="Testing". That I can then render it from the template
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email').lower()
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        username = request.form.get('username')
        gender = request.form.get('gender')
        birth_date = request.form.get('birthDate')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user_type = request.form.get('user_type')
        is_premium = request.form.get('is_premium')
        month_sub = request.form.get('month_sub')
        nickname = request.form.get('nickname')

        # We can check that certain requirements are met such as the minimum length etcetera and send to the user an
        # error message. We can flash the message
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')
        elif len(first_name) == 0:
            flash('First name field can\'t be empty.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 characters.', category='error')
        elif len(last_name) == 0:
            flash('Last name field can\'t be empty.', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 characters.', category='error')
        elif len(email) == 0:
            flash('Email field can\'t be empty.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(password1) == 0:
            flash('Password field can\'t be empty.', category='error')
        elif len(password2) == 0:
            flash('Confirm password field can\'t be empty.', category='error')
        elif len(password1) < 6:
            flash('Password must be at least 6 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif gender == "none":
            flash('Select a gender.', category='error')
        elif user_type == "none":
            flash('Select your user type.', category='error')
        elif user_type == "listener" and is_premium == "none":
            flash('Select a membership type.', category='error')
        elif user_type == "listener" and is_premium == "yes" and month_sub == "none":
            flash('Select how many months you want to subscribe for the Premium membership.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, last_name=last_name, username=username, gender=gender,
                            birth_date=birth_date,
                            password=generate_password_hash(
                                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
