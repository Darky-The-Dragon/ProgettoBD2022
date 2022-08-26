# This is where we create our database models
# Let's make a database for our users
# This imports the database from init.py

from flask_login import UserMixin
from sqlalchemy import func, CheckConstraint

from . import db


# Defining of table
class User(db.Model, UserMixin):
    __tablename__ = "users"

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
    listener = db.relationship('Listener', back_populates='user', lazy=True, cascade='all,delete')
    artist = db.relationship('Artist', back_populates='user', lazy=True, cascade='all,delete')


class Listener(db.Model):
    __tablename__ = 'listeners'
    id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    user = db.relationship('User', back_populates='listener', lazy=True)
    non_premium = db.relationship('Non_Premium', back_populates='listener', lazy=True, cascade='all,delete')
    premium = db.relationship('Premium', back_populates='listener', lazy=True, cascade='all,delete')
    playlist = db.relationship('Playlist', back_populates='listener', lazy=True, cascade='all,delete')


class Non_Premium(db.Model):
    __tablename__ = 'non_premiums'
    id = db.Column(db.Integer, db.ForeignKey('listeners.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    listener = db.relationship('Listener', back_populates='non_premium', lazy=True)


class Premium(db.Model):
    __tablename__ = 'premiums'

    id = db.Column(db.Integer, db.ForeignKey('listeners.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    reg_date = db.Column(db.Date, nullable=False)
    month_sub = db.Column(db.Integer, nullable=False)

    listener = db.relationship('Listener', back_populates='premium', lazy=True)


class Artist(db.Model):
    __tablename__ = "artists"

    id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADES'), primary_key=True, nullable=False)
    n_songs = db.Column(db.Integer, nullable=False)  # Si potrebbe togliere e usare una query
    n_listeners = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', back_populates='artist', lazy=True, cascade='all,delete')
    album = db.relationship('Album', back_populates='artist', lazy=True, cascade='all,delete')
    song = db.relationship('Song', back_populates='artist', lazy=True, cascade='all,delete')


songs_playlist = db.Table('songs_playlists',
                          db.Column('id_playlist', db.Integer, db.ForeignKey('playlists.id', onupdate='CASCADE'),
                                    primary_key=True,
                                    nullable=False),
                          db.Column('id_song', db.Integer, db.ForeignKey('songs.id', onupdate='CASCADE'),
                                    primary_key=True, nullable=False),
                          )

songs_albums = db.Table('songs_albums',
                        db.Column('id_album', db.Integer, db.ForeignKey('albums.id', onupdate='CASCADE'),
                                  primary_key=True,
                                  nullable=False),
                        db.Column('id_song', db.Integer, db.ForeignKey('songs.id', onupdate='CASCADE'),
                                  primary_key=True, nullable=False),
                        )


class Playlist(db.Model):
    __tablename__ = "playlists"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    id_listener = db.Column(db.Integer, db.ForeignKey('listeners.id', ondelete='CASCADE'), nullable=False)
    playlist_name = db.Column(db.String(150), nullable=False)
    n_songs = db.Column(db.Integer, nullable=False)  # Da togliere, si puo usare una query
    description = db.Column(db.String(500), nullable=False)
    create_date = db.Column(db.Date, nullable=False)
    listener = db.relationship('Listener', back_populates='playlist', lazy=True, cascade='all,delete')
    song = db.relationship('Song', secondary=songs_playlist, back_populates='playlist', lazy=True,
                           cascade='save-update')


class Album(db.Model):
    __tablename__ = "albums"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    id_artist = db.Column(db.Integer, db.ForeignKey('artists.id', ondelete='CASCADE'), nullable=False)
    album_name = db.Column(db.String(150), nullable=False)
    n_songs = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    launch_date = db.Column(db.Date, nullable=False)
    artist = db.relationship('Artist', back_populates='album', lazy=True, cascade='all,delete')
    song = db.relationship('Song', secondary=songs_albums, back_populates='album', lazy=True, cascade='save-update')


class Song(db.Model):
    __tablename__ = "songs"
    __table_args__ = (
        CheckConstraint('exp_date > launch_date', name='check1'),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    id_artist = db.Column(db.Integer, db.ForeignKey('artists.id', ondelete='CASCADE'), nullable=False)
    launch_date = db.Column(db.Date, nullable=False)
    exp_date = db.Column(db.Date, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    duration = db.Column(db.Time, nullable=False)
    n_replays = db.Column(db.Integer, nullable=False)
    artist = db.relationship('Artist', back_populates='song', lazy=True, cascade='all,delete')
    album = db.relationship('Album', secondary=songs_albums, back_populates='song', lazy=True, cascade='save-update')
    playlist = db.relationship('Playlist', secondary=songs_playlist, back_populates='song', lazy=True,
                               cascade='save-update')


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


def get_artist_data(artist_id):
    return db.session.query(Artist).filter_by(id=artist_id).first()


def get_artist_name(artist_id):
    if db.session.query(Artist.id).filter_by(id=artist_id).first() is not None:
        artist = db.session.query(User).filter_by(id=artist_id).first()
        return artist.username
    else:
        return None


def get_listener_name(listener_id):
    if db.session.query(Listener.id).filter_by(id=listener_id).first() is not None:
        listener = db.session.query(User).filter_by(id=listener_id).first()
        return listener.username
    else:
        return None


def album_list(id_artist):
    values = db.session.query(Album).filter_by(id_artist=id_artist).all()
    result = []
    for i in values:
        result.append(i)
    return result


def playlist_list(id_listener):
    values = db.session.query(Playlist).filter_by(id_listener=id_listener).all()
    result = []
    for i in values:
        result.append(i)
    return result


def song_list(id_artist):
    values = db.session.query(Song).filter_by(id_artist=id_artist).all()
    result = []
    for i in values:
        result.append(i)
    return result


def song_list_album(id_album, id_artist):
    values = db.session.query(Song).filter_by(id_artist=id_artist).join(songs_albums).filter_by(id_album=id_album).all()
    print(values)
    return values


def song_list_playlist(id_playlist):
    values = db.session.query(Song).join(songs_playlist).filter_by(id_playlist=id_playlist).all()
    return values


def search_a_song(search):
    if search:
        found = db.session.query(Song).filter(func.lower(Song.title).contains(func.lower(search))).all()
    return found


def search_an_album(search):
    if search:
        found = db.session.query(Album).filter(func.lower(Album.album_name).contains(func.lower(search))).all()
    return found


def search_an_artist(search):
    if search:
        found = db.session.query(User).join(Artist, Artist.id == User.id).filter(
            func.lower(User.username).contains(func.lower(search)))

        test = found.all()
    return test


def user_delete(user_id):
    if user_id:
        to_delete = db.session.query(User).filter_by(id=user_id).first()
        if to_delete:
            db.session.delete(to_delete)
            db.session.commit()

