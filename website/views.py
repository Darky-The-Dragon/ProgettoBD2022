# We need to import render_template to render it
from flask import Blueprint, render_template, request, flash, jsonify, url_for, redirect
from flask_login import login_required, current_user
from .models import user_type, search_a_song, search_an_album
from .models import Note, Song
from . import db
import operator
import json


# The URL that our website has

# Define of blueprint
views = Blueprint('views', __name__)


# Decorator and definition of root
# / is the URL
@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    type = user_type(current_user.id)


    searched = request.args.get('searched')

    if searched:
        return redirect(url_for('searched.searched_results', search=searched))


    return render_template("home.html", user=current_user, user_type=type)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})







