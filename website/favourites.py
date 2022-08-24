from flask import Blueprint, render_template
from flask_login import login_required, current_user

from .models import Playlist, Listener, get_listener_name, song_list_playlist, user_type

favourites = Blueprint("favourites", __name__, static_folder='static', template_folder='templates')


@favourites.route('/user/favourites/')
@login_required
def favourites_data():
    this_favourites = Playlist.query.filter_by(id_listener=current_user.id).filter(Playlist.playlist_name.contains("Favourite Songs")).first()

    if this_favourites is None:
        return render_template("404.html")

    listener = Listener.query.filter_by(id=this_favourites.id_listener).first()
    listener_nickname = get_listener_name(listener.id)
    song_list = song_list_playlist(this_favourites.id)
    print(song_list)
    return render_template("playlist_metadata.html", user=current_user, user_type=user_type(current_user.id),
                           playlist=this_favourites, listener=listener_nickname,
                           songs=song_list)