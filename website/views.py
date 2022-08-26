# We need to import render_template to render it

from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import login_required, current_user

from .models import user_type

# The URL that our website has

# Define of blueprint
views = Blueprint('views', __name__)


# Decorator and definition of root
# / is the URL
@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    searched = request.args.get('searched')

    if searched:
        return redirect(url_for('searched.searched_results', search=searched))

    return render_template("home.html", user=current_user, user_type=user_type(current_user.id))
