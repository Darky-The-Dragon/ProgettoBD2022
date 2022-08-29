from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from sqlalchemy import update, select

from . import db
from .models import Playlist, Listener, get_listener_name, song_list_playlist, user_type, favourites_artist, Artist, \
    get_artist_data, album_list, song_list
from .song import remove_from_favourites, play_song

favourites = Blueprint("favourites", __name__, static_folder='static', template_folder='templates')


@favourites.route('/user/favourites/')
@login_required
def favourites_data():
    this_favourites = Playlist.query.filter_by(id_listener=current_user.id).filter(
        Playlist.playlist_name.contains("Favourite Songs")).first()

    if this_favourites is None:
        return render_template("404.html")

    song = request.args.get("play_song")
    if song:
        play_song(song)

    favourite_song = request.args.get("remove_favourite_song")
    if favourite_song:
        remove_from_favourites(favourite_song)

    listener = Listener.query.filter_by(id=this_favourites.id_listener).first()
    listener_nickname = get_listener_name(listener.id)
    song_list = song_list_playlist(this_favourites.id)

    return render_template("playlist_metadata.html", user=current_user, user_type=user_type(current_user.id),
                           playlist=this_favourites, listener=listener_nickname,
                           songs=song_list)




@favourites.route('/user/add_favourites/<id_artist>', methods=['GET', 'POST'])
@login_required
def add_favourite_artist(id_artist):
    listener_artist = select([favourites_artist]).where(favourites_artist.c.id_artist == id_artist,
                                                        favourites_artist.c.id_listener == current_user.id)
    s = db.session.execute(listener_artist).first()
    if s:
        flash('Artist is already inserted', category='error')

    else:
        new_favourite = favourites_artist.insert().values(id_artist=id_artist, id_listener=current_user.id)
        db.session.execute(update(Artist).where(Artist.id == id_artist).values(n_listeners=Artist.n_listeners + 1))
        db.session.execute(new_favourite)
        db.session.commit()
        flash('Artist added to followed', category='success')

    return (''), 204


@favourites.route('/user/remove_favourites/<int:id_artist>', methods=['GET'])
@login_required
def remove_favourite_artist(id_artist):

    listener_artist = select([favourites_artist]).where(favourites_artist.c.id_artist == id_artist,
                                                        favourites_artist.c.id_listener == current_user.id)
    s = db.session.execute(listener_artist).first()
    if s is None:
        flash('This artist isn\'t in your favourites', category='error')
    else:
        to_delete = favourites_artist.delete().where(favourites_artist.c.id_artist == id_artist,
                                                     favourites_artist.c.id_listener == current_user.id)
        db.session.execute(to_delete)
        db.session.execute(update(Artist).where(Artist.id == id_artist).values(n_listeners=Artist.n_listeners - 1))

        db.session.commit()
        flash('Artist remove to followed', category='error')

    return (''), 204