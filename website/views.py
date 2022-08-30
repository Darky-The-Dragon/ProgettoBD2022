# We need to import render_template to render it

from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import login_required, current_user

from .models import *
from .song import play_song, add_favourite

# The URL that our website has

# Define of blueprint
views = Blueprint('views', __name__)


# Decorator and definition of root
# / is the URL
@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    searched = request.args.get('searched')
    recommendation = recommended(current_user.id)

    if searched:
        return redirect(url_for('searched.searched_results', search=searched))

    add_favourite_song = request.args.get("add_favourite_song")
    if add_favourite_song:
        add_favourite(add_favourite_song)

    song = request.args.get("play_song")
    if song:
        play_song(song)

    return render_template("home.html", user=current_user, user_type=user_type(current_user.id), recommendation=recommendation)
