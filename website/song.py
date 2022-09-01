from flask import Blueprint, render_template, flash, url_for
from flask_login import login_required, current_user
from sqlalchemy import select, update
import operator
from .models import db, Artist, Playlist, Song, get_artist_name, user_type, songs_playlist, get_listener_name, Listener, \
    song_list_playlist

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
                           song=this_song, artist=artist_nickname, owner=current_user.id == this_song.id_artist)


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


@song.route('/play_song/<int:id_song>', methods=['GET', 'POST'])
@login_required
def play_song(id_song):
    # CODE GOES HERE
    # n_replays = db.Column(db.Integer, nullable=False)
    if operator.not_(Song.query.filter_by(id=id_song, id_artist=current_user.id).first()):
        stmt = update(Song).where(Song.id == id_song).values(n_replays=Song.n_replays + 1)
        db.session.execute(stmt)
        db.session.commit()

    return (''), 204


@song.route('/remove_from_favourite/<int:id_song>', methods=['DELETE'])
@login_required
def remove_from_favourites(id_song):
    playlist = Playlist.query.filter_by(id_listener=current_user.id, playlist_name="Favourite Songs").first()
    if playlist:
        to_delete = songs_playlist.delete().where(songs_playlist.c.id_song == id_song,
                                                  songs_playlist.c.id_playlist == playlist.id)

        db.session.execute(to_delete)
        db.session.execute(update(Playlist).where(Playlist.id == playlist.id).values(n_songs=Playlist.n_songs-1))
        db.session.commit()
        flash('Song successfully removed your favourites!', category='success')

    return (''), 204


@song.route('/remove_from_playlist/<int:id_playlist>/<int:id_song>', methods=['DELETE'])
@login_required
def remove_from_playlist(id_song, id_playlist):
    playlist = Playlist.query.filter_by(id_listener=current_user.id, id=id_playlist).first()

    if playlist:
        to_delete = songs_playlist.delete().where(songs_playlist.c.id_song == id_song,
                                                  songs_playlist.c.id_playlist == playlist.id)

        db.session.execute(to_delete)
        db.session.execute(update(Playlist).where(Playlist.id == playlist.id).values(n_songs=Playlist.n_songs-1))
        db.session.commit()
        flash('Song successfully removed your playlist!', category='success')

    return (''), 204
