from flask import Blueprint, flash, request, url_for, render_template
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect

from . import db
from .models import User, user_type, is_premium, get_months, user_delete

user = Blueprint("user", __name__, static_folder='static', template_folder='templates')


# Route che porta al profilo principale dell'utente
@user.route('user/profile/<int:user_id>')
@login_required
def userprofile(user_id):
    this_user = User.query.filter_by(id=user_id).first()

    if this_user is None:
        return render_template("404.html", user=current_user, user_type=user_type(current_user.id))

    membership = is_premium(user_id)
    months = get_months(current_user.id)

    return render_template("profile.html", user=this_user, user_type=user_type(current_user.id), membership=membership,
                           months=months)


# Funzione per la modifica della password
@user.route('/user/modify_password', methods=['GET', 'POST'])
@login_required
def modify_password():
    if request.method == 'POST':
        this_user = User.query.filter_by(id=current_user.id).first()
        email = request.form.get('email')
        old_pw = request.form.get('old_pw')
        new_pw1 = request.form.get('password1')
        new_pw2 = request.form.get('password2')

        if len(email) == 0:
            flash('Email field can\'t be empty.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(old_pw) == 0:
            flash('Old password field can\'t be empty.', category='error')
        elif email != this_user.email or not check_password_hash(this_user.password, old_pw):
            flash("Wrong credential. Check again and retry", category='error')
        elif len(new_pw1) == 0:
            flash('New password field can\'t be empty.', category='error')
        elif len(new_pw2) == 0:
            flash('Confirm password field can\'t be empty.', category='error')
        elif len(new_pw1) < 6:
            flash('Password must be at least 6 characters.', category='error')
        elif new_pw1 != new_pw2:
            flash('Passwords don\'t match.', category='error')
        elif old_pw == new_pw1:
            flash('New password can\'t be the same as the old password', category='error')
        else:
            try:
                this_user.password = generate_password_hash(new_pw1, method='sha256')
                db.session.commit()
                flash("Password changed successfully", category='success')
            except:
                db.session.rollback()
                flash("An error occurred. Password couldn't be changed", category='error')
            return redirect(url_for('user.userprofile', user_id=current_user.id))
    return render_template('password_change.html', user=current_user)


@user.route('user/delete_account/<int:user_id>')
@login_required
def delete_account(user_id):
    user_delete(user_id)
    flash("Account deleted", category='success')
    return redirect(url_for('auth.login'))
