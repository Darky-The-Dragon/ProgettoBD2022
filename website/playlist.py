from flask import Blueprint, render_template
from flask_login import login_required, current_user

from .models import Playlist, Listener, get_listener_name, song_list_playlist, user_type

playlist = Blueprint("playlist", __name__, static_folder='static', template_folder='templates')


@playlist.route('/user/playlist/<int:id_playlist>')
@login_required
def album_data(id_playlist):
    this_playlist = Playlist.query.filter_by(id=id_playlist).first()

    if this_playlist is None:
        return render_template("404.html")

    listener = Listener.query.filter_by(id=this_playlist.id_listener).first()
    listener_nickname = get_listener_name(listener.id)
    song_list = song_list_playlist(this_playlist.id, listener.id)
    print(song_list)
    return render_template("playlist_metadata.html", user=current_user, user_type=user_type(current_user.id),
                           playlist=this_playlist, listener=listener_nickname,
                           songs=song_list)
