import operator
from datetime import date

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required

from .models import *

# The URL that our website has

# Define of blueprint
add_song = Blueprint('add_song', __name__)


# fatti fare dei check e dei trigger da luca che controlli che le exp_date

@add_song.route('user/dashboard/add_song/', methods=['GET', 'POST'])
@login_required
def insert_song():

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
            new_song = Song(id_artist=current_user.id, launch_date=date.today(),
                            exp_date=ex_date, title=title, duration=duration, n_replays=0)
            db.session.add(new_song)
            db.session.commit()
            flash('Song added!', category='success')
            return redirect(url_for('add_song.insert_song'))

    return render_template("add_song.html", user=current_user, user_type=user_type(current_user.id))

@add_song.route('user/dashboard/add_song/<album_id>', methods=['GET', 'POST'])
@login_required
def insert_song_album(album_id):
    album = Album.query.filter_by(id=album_id).first()  # per avere tutti i valori della tupla

    song_list = title_in_album(album.id, current_user.id)

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
            new_song = Song(id_artist=current_user.id, id_album=album.id, launch_date=date.today(),
                            exp_date=ex_date, title=title, duration=duration, n_replays=0)
            db.session.add(new_song)
            db.session.commit()
            flash('Song added!', category='success')
            return redirect(url_for('add_song.insert_song', album_id=album.id))

    return render_template("add_song.html", user=current_user, user_type=user_type(current_user.id), album=album, songs=song_list)
