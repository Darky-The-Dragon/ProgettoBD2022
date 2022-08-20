from datetime import date
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required

from .models import *

# The URL that our website has

# Define of blueprint
dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/user/dashboard/')
@login_required
def dashboard_load():
    album = album_list(current_user.id)
    return render_template("dashboard.html", user=current_user, user_type=user_type(current_user.id), album=album)


@dashboard.route('/user/dashboard/add_album', methods=['GET', 'POST'])
@login_required
def insert_album():
    album = album_list(current_user.id)

    if request.method == 'POST':
        album_name = request.form.get('Album_name')
        n_songs = request.form.get('n_songs')
        album_c = (request.form.get('album_c'))
        album = Album.query.filter_by(album_name=album_name).first()

        if album_c:
            return redirect(url_for('add_song.insert_song', album_id=album_c))
        elif album:
            flash('Album already exists', category='error')
        elif operator.not_(album_name):
            flash('Please, insert the album\'s name', category='error')
        elif operator.not_(n_songs):
            flash('Please, insert the number of the songs', category='error')
        elif len(album_name) == 0:
            flash('Album name must be greater than 0 characters', category='error')
        elif int(n_songs) <= 0:
            flash('Number of songs must be a positive value', category='error')
        else:
            new_album = Album(id_artist=current_user.id, launch_date=date.today(),
                              n_songs=n_songs, album_name=album_name)
            db.session.add(new_album)
            db.session.commit()
            flash('Album added!', category='success')
            return redirect(url_for('add_album.insert_album'))

    return render_template("dashboard.html", user=current_user, user_type=user_type(current_user.id), album=album)
