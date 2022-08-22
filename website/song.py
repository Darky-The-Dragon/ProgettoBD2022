from flask import Blueprint, render_template
from flask_login import login_required, current_user

from .models import Song, Artist, get_artist_name, user_type

song = Blueprint("song", __name__, static_folder='static', template_folder='templates')


@song.route('/song/<int:song_id>')
@login_required
def song_data(song_id):
    this_song = Song.query.filter_by(id=song_id).first()

    if this_song is None:
        return render_template("404.html")

    artist = Artist.query.filter_by(id=this_song.id_artist).first()
    artist_nickname = get_artist_name(artist.id)

    return render_template("song_metadata.html", user=current_user, user_type=user_type(current_user.id),
                           song=this_song, artist=artist_nickname)
