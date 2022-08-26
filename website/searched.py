from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import login_required, current_user

from .models import *
from .song import play_song

searched = Blueprint('searched', __name__)


@searched.route('/search/<search>', methods=['GET', 'POST'])
def searched_results(search):
    searched_1 = search_an_artist(search)
    searched_2 = search_an_album(search)
    searched_3 = search_a_song(search)

    return render_template("search.html", user=current_user, user_type=user_type(current_user.id), search=search,
                           searched_1=searched_1, searched_2=searched_2, searched_3=searched_3)


@searched.route('user/playlist/add_song/<id_playlist>', methods=['GET', 'POST'])
@login_required
def search_song_playlist(id_playlist):
    searched = request.args.get('searched')

    song = request.args.get("play_song")
    if song:
        play_song(song)

    if searched:
        return redirect(url_for('add_song.insert_song_playlist', search=searched, id_playlist=id_playlist))

    return render_template('song_in_playlist.html', user=current_user)
# searched = Blueprint('searched', __name__)

# @searched.route('/search/<search>', methods = ['GET', 'POST'])
# def searched_results(search):

#    searched_1 = search_a_song(search)
#   searched_2 = search_an_album(search)


#  return render_template("search.html", user=current_user, searched_1=searched_1, searched_2=searched_2)
