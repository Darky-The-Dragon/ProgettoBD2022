from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

from .models import *
from .song import play_song

# The URL that our website has

# Define of blueprint
dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/user/dashboard/')
@login_required
def dashboard_load():
    artist = get_artist_data(current_user.id)
    albums = album_list(current_user.id)
    n_album = len(albums)
    songs = song_list(current_user.id)
    n_songs = len(songs)

    song = request.args.get("play_song")
    if song:
        play_song(song)

    return render_template("dashboard.html", user=current_user, user_type=user_type(current_user.id), artist=artist,
                           albums=albums, n_album=n_album, songs=songs, n_songs=n_songs)
