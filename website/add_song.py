import operator
from datetime import date

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy import update

from .models import *

# The URL that our website has

# Define of blueprint
add_song = Blueprint('add_song', __name__)


# fatti fare dei check e dei trigger da luca che controlli che le exp_date

@add_song.route('user/dashboard/add_song/', methods=['GET', 'POST'])
@login_required
def create_song():
    title = request.form.get('sname')
    duration = request.form.get('duration')
    ex_date = request.form.get('ex_date')

    song = Song.query.filter_by(title=title).first()
    if request.method == 'POST':
        if song:
            flash('Song already exists', category='error')
        elif operator.not_(title):
            flash('Please, type the title of your song', category='error')
        elif operator.not_(duration):
            flash('Please, type the duration of your song', category='error')
        elif operator.not_(ex_date):
            flash('Please, type the expiration date of your song', category='error')
        else:
            try:
                new_song = Song(id_artist=current_user.id, launch_date=date.today(),
                                exp_date=ex_date, title=title, duration=duration, n_replays=0)
                db.session.add(new_song)
                db.session.commit()
                flash('Song added!', category='success')
            except:
                db.session.rollback()
                flash('Expiration date must be greater then current date', category='error')
            return redirect(url_for('add_song.create_song'))

    return render_template("add_song.html", user=current_user, user_type=user_type(current_user.id), album=None)


@add_song.route('user/dashboard/add_song/<id_album>', methods=['GET', 'POST'])
@login_required
def insert_song_album(id_album):
    album = Album.query.filter_by(id=id_album).first()  # per avere tutti i valori della tupla
    song_id = request.form.get('song_id')
    all_songs = song_list(current_user.id)

    if album is None:
        return render_template("404.html", user=current_user, user_type=user_type(current_user.id))

    song_list_ = song_list_album(id_album, current_user.id)
    title = request.form.get('sname_')
    duration = request.form.get('duration_')
    ex_date = request.form.get('ex_date_')

    if song_id:
        val = db.session.query(Song).join(songs_albums).filter_by(id_album=id_album, id_song=song_id).all()
        if val:
            flash('Song already in this album', category='error')
            return redirect(url_for('add_song.insert_song_album', id_album=album.id))
        else:
            new_songs_album = songs_albums.insert().values(id_album=id_album, id_song=song_id)
            db.session.execute(new_songs_album)
            db.session.execute(update(Album).where(Album.id == id_album).values(n_songs=Album.n_songs + 1))
            db.session.commit()
            flash('Song added!', category='success')
            return redirect(url_for('add_song.insert_song_album', id_album=album.id))

    song = Song.query.filter_by(title=title).first()
    if request.method == 'POST':
        if song:
            flash('Song already exists', category='error')
        elif operator.not_(title):
            flash('Please, type the title of your song', category='error')
        elif operator.not_(duration):
            flash('Please, type the duration of your song', category='error')
        elif operator.not_(ex_date):
            flash('Please, type the expiration date of your song', category='error')
        else:
            try:
                new_song = Song(id_artist=current_user.id, launch_date=date.today(),
                                exp_date=ex_date, title=title, duration=duration, n_replays=0)
                db.session.add(new_song)
                db.session.commit()
                new_songs_album = songs_albums.insert().values(id_album=id_album, id_song=new_song.id)
                db.session.execute(update(Album).where(Album.id == id_album).values(n_songs=Album.n_songs + 1))
                db.session.execute(new_songs_album)
                db.session.commit()
                flash('Song added!', category='success')
            except:
                db.session.rollback()
                flash('Expiration date must be greater then current date', category='error')
            return redirect(url_for('add_song.insert_song_album', id_album=album.id))

    return render_template("add_song.html", user=current_user, user_type=user_type(current_user.id), album=album,
                           songs=song_list_, all_songs=all_songs)


@add_song.route('user/playlist/add_song/<id_playlist>/<search>', methods=['GET', 'POST'])
@login_required
def insert_song_playlist(id_playlist, search):
    searched = search_a_song(search)
    value = request.args.get('searched')

    if request.method == 'POST':
        id_song = request.form.get('song_id')

        if db.session.query(songs_playlist).filter_by(id_playlist=id_playlist, id_song=id_song).first():
            flash('Song already in playlist', category='error')
            return redirect(url_for('add_song.insert_song_playlist', id_playlist=id_playlist, search=search))
        else:
            new_song_playlist = songs_playlist.insert().values(id_song=id_song, id_playlist=id_playlist)
            db.session.execute(update(Playlist).where(Playlist.id == id_playlist).values(n_songs=Playlist.n_songs + 1))
            db.session.execute(new_song_playlist)
            db.session.commit()

            flash('Song added!', category='success')
            return redirect(url_for('add_song.insert_song_playlist', id_playlist=id_playlist, search=search))

    if value:
        return redirect(url_for('add_song.insert_song_playlist', id_playlist=id_playlist, search=value))

    return render_template("song_in_playlist.html", user=current_user, user_type=user_type(current_user.id),
                           search=search,
                           searched=searched)
