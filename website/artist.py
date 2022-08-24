from flask import Blueprint, render_template
from flask_login import current_user, login_required

from .models import *

# The URL that our website has

# Define of blueprint
artist = Blueprint('artist', __name__)


@artist.route('/artist/<int:id_artist>')
@login_required
def artist_info(id_artist):
    artist_data = get_artist_data(id_artist)
    artist_name = get_artist_name(id_artist)
    albums = album_list(id_artist)
    print(albums[0].album_name)
    n_album = len(albums)
    songs = song_list(id_artist)
    n_songs = len(songs)
    return render_template("dashboard.html", user=current_user, user_type=user_type(current_user.id), artist=artist_data,
                           artist_name=artist_name, albums=albums, n_album=n_album, songs=songs, n_songs=n_songs)