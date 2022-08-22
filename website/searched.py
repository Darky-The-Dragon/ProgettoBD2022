from flask import Blueprint, render_template
from flask_login import current_user

from .models import *

searched = Blueprint('searched', __name__)


@searched.route('/search/<search>', methods=['GET', 'POST'])
def searched_results(search):
    searched_1 = search_a_song(search)
    searched_2 = search_an_album(search)

    return render_template("search.html", user=current_user, user_type=user_type(current_user.id),
                           searched_1=searched_1, searched_2=searched_2)
