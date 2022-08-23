from flask import Blueprint, render_template
from flask_login import login_required, current_user

from .models import Album, Artist, get_artist_name, song_list_album, user_type

album = Blueprint("album", __name__, static_folder='static', template_folder='templates')


@album.route('/user/album/<int:album_id>')
@login_required
def album_info(album_id):
    this_album = Album.query.filter_by(id=album_id).first()

    if this_album is None:
        return render_template("404.html")

    artist = Artist.query.filter_by(id=this_album.id_artist).first()
    artist_nickname = get_artist_name(artist.id)
    song_list = song_list_album(this_album.id, artist.id)
    print(song_list)
    return render_template("album_metadata.html", user=current_user, user_type=user_type(current_user.id),
                           album=this_album, artist=artist_nickname,
                           songs=song_list)
