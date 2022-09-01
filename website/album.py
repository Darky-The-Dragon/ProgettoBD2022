from flask import Blueprint, render_template, request, flash, url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from . import db
from .models import Album, Artist, get_artist_name, song_list_album, user_type
from .song import add_favourite, play_song

album = Blueprint("album", __name__, static_folder='static', template_folder='templates')


@album.route('/album/<int:album_id>', methods=['GET'])
@login_required
def album_info(album_id):
    this_album = Album.query.filter_by(id=album_id).first()

    if this_album is None:
        return render_template("404.html")

    add_favourite_song = request.args.get("add_favourite_song")
    if add_favourite_song:
        add_favourite(add_favourite_song)

    song = request.args.get("play_song")
    if song:
        play_song(song)

    delete = request.args.get("delete")
    if delete:
        delete_album(delete)

    artist_data = Artist.query.filter_by(id=this_album.id_artist).first()
    artist_nickname = get_artist_name(artist_data.id)
    song_list = song_list_album(this_album.id, artist_data.id)

    return render_template("album_metadata.html", user=current_user, user_type=user_type(current_user.id),
                           album=this_album, artist=artist_nickname, artist_id=artist_data.id,
                           songs=song_list, owner=current_user.id == this_album.id_artist)


@album.route('/album/delete_album/<int:album_id>', methods=['DELETE'])
@login_required
def delete_album(album_id):
    to_delete = Album.query.filter_by(id=album_id).first()
    if to_delete:
        db.session.delete(to_delete)
        db.session.commit()
        flash("Album successfully deleted", category='success')
    else:
        db.session.rollback()
        flash("Album already deleted", category='error')
        return redirect(url_for('album.album_info'))

    return (''), 204
