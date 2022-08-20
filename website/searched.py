from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from .models import *
import operator

searched = Blueprint('searched', __name__)

@searched.route('/search/<search>', methods = ['GET', 'POST'])
def searched_results(search):

    searched_1 = search_a_song(search)
    searched_2 = search_an_album(search)

    return render_template("search.html", user=current_user, searched_1=searched_1, searched_2=searched_2)