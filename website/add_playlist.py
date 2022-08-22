from datetime import date

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required

from .models import *

# The URL that our website has

# Define of blueprint
add_playlist = Blueprint('add_playlist', __name__)


@add_playlist.route('/user/playlist/add_playlist', methods=['GET', 'POST'])
@login_required
def insert_playlist():
    playlist = playlist_list(current_user.id)

    if request.method == 'POST':
        playlist_name = request.form.get('Album_name')
        n_songs = request.form.get('n_songs')
        playlist_c = (request.form.get('playlist_c'))

        if playlist_c and playlist_c != "none":
            return redirect(url_for('add_song.insert_song_album', id_album=playlist_c))
        elif Playlist.query.filter_by(playlist_name=playlist_name).first() is not None:
            flash('Playlist with such name already exists', category='error')
        elif operator.not_(playlist_name):
            flash('Please, insert the playlist\'s name', category='error')
        elif operator.not_(n_songs):
            flash('Please, insert the number of songs', category='error')
        elif len(playlist_name) == 0:
            flash('Playlist name field can\'t be empty', category='error')
        elif len(playlist_name) < 2:
            flash('Playlist name must be at least 2 characters.', category='error')
        elif int(n_songs) <= 0:
            flash('Number of songs must be a positive value', category='error')
        else:
            new_playlist = Playlist(id_listener=current_user.id, playlist_name=playlist_name, n_songs=n_songs, create_date=date.today())
            db.session.add(new_playlist)
            db.session.commit()
            flash('Playlist created!', category='success')
            return redirect(url_for('add_playlist.insert_playlist', playlist=playlist))

    return render_template("add_playlist.html", user=current_user, user_type=user_type(current_user.id), playlist=playlist)
