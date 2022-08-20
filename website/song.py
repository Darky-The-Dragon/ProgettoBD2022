from flask import Blueprint, flash, request, url_for, render_template
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect

from . import db
from .models import Song, Artist, get_artist_name

song = Blueprint("song", __name__, static_folder='static', template_folder='templates')


@song.route('/song/<int:song_id>')
@login_required
def song_data(song_id):
    this_song = Song.query.filter_by(id=song_id).first()
    artist = Artist.query.filter_by(id=this_song.id_artist).first()
    artist_nickname = get_artist_name(artist.id)
    return render_template("song_metadata.html", user=current_user, song=this_song, artist=artist_nickname)
