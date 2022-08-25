from flask import Blueprint, render_template
from flask_login import login_required, current_user

from .models import Playlist, Listener, get_listener_name, song_list_playlist, playlist_list, user_type

playlist = Blueprint("playlist", __name__, static_folder='static', template_folder='templates')


@playlist.route('/user/playlist')
@login_required
def playlist_data():
    playlists = playlist_list(current_user.id)

    listener = Listener.query.filter_by(id=current_user.id).first()
    listener_nickname = get_listener_name(listener.id)

    return render_template("playlist_list.html", user=current_user, user_type=user_type(current_user.id),
                           playlists=playlists, listener=listener_nickname)


@playlist.route('/user/playlist/<int:id_playlist>')
@login_required
def playlist_info(id_playlist):
    this_playlist = Playlist.query.filter_by(id=id_playlist).first()

    if this_playlist is None:
        return render_template("404.html")

    listener = Listener.query.filter_by(id=this_playlist.id_listener).first()
    listener_nickname = get_listener_name(listener.id)
    song_list = song_list_playlist(this_playlist.id)

    return render_template("playlist_metadata.html", user=current_user, user_type=user_type(current_user.id),
                           playlist=this_playlist, listener=listener_nickname, songs=song_list)
