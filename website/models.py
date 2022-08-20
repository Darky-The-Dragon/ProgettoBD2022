# This is where we create our database models
# Let's make a database for our users
# This imports the database from init.py
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import operator


# Defining of table
class User(db.Model, UserMixin):
    # Defining fields
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # We can define the maximum length and say if it's unique or not
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150))
    gender = db.Column(db.String(150), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    # We need to specify the relationship
    notes = db.relationship('Note')


class Listener(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)


class Non_Premium(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('listener.id'), primary_key=True, nullable=False)


class Premium(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('listener.id'), primary_key=True, nullable=False)
    reg_date = db.Column(db.Date, nullable=False)
    month_sub = db.Column(db.Integer, nullable=False)


class Artist(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    n_songs = db.Column(db.Integer, nullable=False)
    n_listeners = db.Column(db.Integer, nullable=False)
    nickname = db.Column(db.String(150))


songs_playlist = db.Table('songs_playlist',
                          db.Column('id_playlist', db.Integer, db.ForeignKey('playlist.id'), primary_key=True,
                                    nullable=False),
                          db.Column('id_song', db.Integer, db.ForeignKey('song.id'), primary_key=True, nullable=False)
                          )

songs_albums = db.Table('songs_albums',
                        db.Column('id_playlist', db.Integer, db.ForeignKey('album.id'), primary_key=True,
                                  nullable=False),
                        db.Column('id_song', db.Integer, db.ForeignKey('song.id'), primary_key=True, nullable=False)
                        )


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    id_listener = db.Column(db.Integer, db.ForeignKey('listener.id'), nullable=False)
    playlist_name = db.Column(db.String(150), nullable=False)
    n_songs = db.Column(db.Integer, nullable=False)
    create_date = db.Column(db.Date, nullable=False)


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    id_artist = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    album_name = db.Column(db.String(150), nullable=False)
    n_songs = db.Column(db.Integer, nullable=False)
    launch_date = db.Column(db.Date, nullable=False)


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    id_artist = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    id_album = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=False)
    launch_date = db.Column(db.Date, nullable=False)
    exp_date = db.Column(db.Date, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    duration = db.Column(db.Time, nullable=False)
    n_replays = db.Column(db.Integer, nullable=False)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(db.String(10000), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    # Use of foreign key to reference another table
    # 1 to many relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# FUNCTIONS ----------------------------------------------------------------------------
# Function that retrieves all users
def user_list():
    users = db.session.query(User.id, User.first_name, User.last_name).all()
    # print(utenti[1])
    print(users)
    return users


def user_type(user_id):
    if db.session.query(Listener.id).filter_by(id=user_id).first() is not None:
        return 0
    elif db.session.query(Artist.id).filter_by(id=user_id).first() is not None:
        return 1


def is_premium(user_id):
    if db.session.query(Non_Premium.id).filter_by(id=user_id).first() is not None:
        return 0
    elif db.session.query(Premium.id).filter_by(id=user_id).first() is not None:
        return 1


def get_months(user_id):
    row = db.session.query(Premium).filter_by(id=user_id).first()
    if row is None:
        return 0
    else:
        return row.month_sub

def album_list(artist_id):
    values = db.session.query(Album).filter_by(id_artist=artist_id).all()
    result = []
    for i in values:
        result.append(i)
    return result

def title_in_album(album_id, user_id):
    values = db.session.query(Song).filter_by(id_album=album_id, id_artist=user_id).all()
    result = []

    for i in values:
       result.append(i.title)
    return result

def search_a_song(song_title):
    if (song_title):
        found = db.session.query(Song.id).filter(Song.title.contains(song_title)).all()
        if operator.not_(found):
           found = db.session.query(Song.id).all()

        return found

def search_an_album(album_name):
    if(album_name):
       found = db.session.query(Album.id).filter(Album.album_name.contains(album_name)).all()
       if operator.not_(found):
          found = db.session.query(Album.id).all()

       return found