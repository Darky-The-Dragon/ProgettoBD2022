from datetime import date
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required

from .models import *

# The URL that our website has

# Define of blueprint
dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/user/dashboard/')
@login_required
def dashboard_load():
    artist = get_artist_data(current_user.id)
    album = album_list(current_user.id)
    n_album = len(album)
    songs = song_list(current_user.id)
    n_songs = len(songs)
    return render_template("dashboard.html", user=current_user, user_type=user_type(current_user.id), artist=artist, n_album=n_album, n_songs=n_songs)
