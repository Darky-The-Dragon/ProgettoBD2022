from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import update

from . import db
from .models import Playlist, Listener, get_listener_name, song_list_playlist, user_type, favourites_artist, Artist
from .song import remove_favourite

favourites = Blueprint("favourites", __name__, static_folder='static', template_folder='templates')


@favourites.route('/user/favourites/')
@login_required
def favourites_data():
    this_favourites = Playlist.query.filter_by(id_listener=current_user.id).filter(
        Playlist.playlist_name.contains("Favourite Songs")).first()

    if this_favourites is None:
        return render_template("404.html")

    listener = Listener.query.filter_by(id=this_favourites.id_listener).first()
    listener_nickname = get_listener_name(listener.id)
    song_list = song_list_playlist(this_favourites.id)

    remove_favourite_song = request.args.get("remove_favourite_song")
    if remove_favourite_song:
        remove_favourite(remove_favourite_song)

    return render_template("playlist_metadata.html", user=current_user, user_type=user_type(current_user.id),
                           playlist=this_favourites, listener=listener_nickname,
                           songs=song_list)


@favourites.route('/user/favourites/<id_artist>')
def add_favourite_artist(id_artist):
    listener_artist = favourites_artist.query.filter_by(id_artist=id_artist, id_listener=current_user.id).first()
    if listener_artist:
        db.session.execute(update(Artist).where(Artist.id == id_artist).values(n_listeners=Artist.n_listeners-1))
        db.session.delete(listener_artist)
        db.session.commit()

    else:
        new_favourite = favourites_artist(id_artist=id_artist, id_listener=current_user.id)
        db.session.execute(update(Artist).where(Artist.id == id_artist).values(n_listeners=Artist.n_listeners + 1))
        db.session.add(new_favourite)
        db.session.commit()

