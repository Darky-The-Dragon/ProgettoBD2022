from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user

from .models import db, Artist, Playlist, Song, get_artist_name, user_type, songs_playlist

song = Blueprint("song", __name__, static_folder='static', template_folder='templates')


@song.route('/song/<int:song_id>')
@login_required
def song_info(song_id):
    this_song = Song.query.filter_by(id=song_id).first()

    if this_song is None:
        return render_template("404.html")

    artist = Artist.query.filter_by(id=this_song.id_artist).first()
    artist_nickname = get_artist_name(artist.id)

    return render_template("song_metadata.html", user=current_user, user_type=user_type(current_user.id),
                           song=this_song, artist=artist_nickname)


@song.route('/add_favourite/<int:id_song>', methods=['GET', 'POST'])
@login_required
def add_favourite(id_song):
    if user_type(current_user.id) == 0:
        print("IT WORKS")
        playlist = Playlist.query.filter_by(id_listener=current_user.id, playlist_name="Favourite Songs").first()

        check = Playlist.query.filter_by(id=playlist.id).join(songs_playlist).filter_by(id_song=id_song).first()

        if check:
            flash('You already added this song to your favourites!', category='error')
        else:
            new_songs_playlist = songs_playlist.insert().values(id_playlist=playlist.id, id_song=id_song)
            db.session.execute(new_songs_playlist)
            db.session.commit()
            flash('Song added to your favourites!', category='success')

    return (''), 204


@song.route('/remove_favourite/<int:id_song>', methods=['DELETE'])
@login_required
def remove_favourite(id_song):
    print("IT DELETED?")
    playlist = Playlist.query.filter_by(id_listener=current_user.id, playlist_name="Favourite Songs").first()
    entry = Playlist.query.filter_by(id=playlist.id).join(songs_playlist).filter_by(id_song=id_song).first()
    songs_playlist.delete(id_song)

    # if entry:
        # entry.remove()
    db.session.commit()
    flash('Song successfully removed your favourites!', category='success')
    #else:
       # flash('Song already removed!', category='error')

    return (''), 204