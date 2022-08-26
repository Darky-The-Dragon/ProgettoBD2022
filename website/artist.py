from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

from .models import *
from .song import add_favourite, play_song

# The URL that our website has

# Define of blueprint
artist = Blueprint('artist', __name__)


@artist.route('/artist/<int:id_artist>', methods=['GET'])
@login_required
def artist_info(id_artist):
    artist_data = get_artist_data(id_artist)
    artist_name = get_artist_name(id_artist)
    albums = album_list(id_artist)
    n_album = len(albums)
    songs = song_list(id_artist)
    n_songs = len(songs)

    add_favourite_song = request.args.get("add_favourite_song")
    if add_favourite_song:
        add_favourite(add_favourite_song)

    song = request.args.get("play_song")
    if song:
        play_song(song)

    return render_template("dashboard.html", user=current_user, user_type=user_type(current_user.id),
                           artist=artist_data,
                           artist_name=artist_name, albums=albums, n_album=n_album, songs=songs, n_songs=n_songs)
