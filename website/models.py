# This is where we create our database models
# Let's make a database for our users
# This imports the database from init.py
import operator

from flask_login import UserMixin


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
    listener = db.relationship('Listener', back_populates='user', lazy=True)
    artist = db.relationship('Artist', back_populates='user', lazy=True)


class Listener(db.Model):
    __tablename__ = 'listeners'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    user = db.relationship('User', back_populates='listener', lazy=True)
    non_premium = db.relationship('Non_Premium', back_populates='listener', lazy=True)
    premium = db.relationship('Premium', back_populates='listener', lazy=True)
    playlist = db.relationship('Playlist', back_populates='listener', lazy=True)


class Non_Premium(db.Model):
    __tablename__ = 'non_premiums'
    id = db.Column(db.Integer, db.ForeignKey('listeners.id'), primary_key=True, nullable=False)
    listener = db.relationship('Listener', back_populates='non_premium', lazy=True)


class Premium(db.Model):
    __tablename__ = 'premiums'

    id = db.Column(db.Integer, db.ForeignKey('listeners.id'), primary_key=True, nullable=False)
    reg_date = db.Column(db.Date, nullable=False)
    month_sub = db.Column(db.Integer, nullable=False)

    listener = db.relationship('Listener', back_populates='premium', lazy=True)


class Artist(db.Model):
    __tablename__ = "artists"

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    n_songs = db.Column(db.Integer, nullable=False)# Si potrebbe togliere e usare una query
    n_listeners = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', back_populates='artist', lazy=True)
    album = db.relationship('Album', back_populates='artist', lazy=True)
    song = db.relationship('Song', back_populates='artist', lazy=True)


songs_playlist = db.Table('songs_playlists',
                          db.Column('id_playlist', db.Integer, db.ForeignKey('playlists.id'), primary_key=True,
                                    nullable=False),
                          db.Column('id_song', db.Integer, db.ForeignKey('songs.id'), primary_key=True, nullable=False),
                          )

songs_albums = db.Table('songs_albums',
                        db.Column('id_album', db.Integer, db.ForeignKey('albums.id'), primary_key=True,
                                  nullable=False),
                        db.Column('id_song', db.Integer, db.ForeignKey('songs.id'), primary_key=True, nullable=False),
                        )


class Playlist(db.Model):
    __tablename__ = "playlists"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    id_listener = db.Column(db.Integer, db.ForeignKey('listeners.id'), nullable=False)
    playlist_name = db.Column(db.String(150), nullable=False)
    n_songs = db.Column(db.Integer, nullable=False)  # Da togliere, si puo usare una query
    create_date = db.Column(db.Date, nullable=False)
    listener = db.relationship('Listener', back_populates='playlist', lazy=True)
    song = db.relationship('Song', secondary=songs_playlist, back_populates='playlist', lazy=True)


class Album(db.Model):
    __tablename__ = "albums"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    id_artist = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    album_name = db.Column(db.String(150), nullable=False)
    n_songs = db.Column(db.Integer, nullable=False)
    launch_date = db.Column(db.Date, nullable=False)
    artist = db.relationship('Artist', back_populates='album', lazy=True)
    song = db.relationship('Song', secondary=songs_albums, back_populates='album', lazy=True)


class Song(db.Model):
    __tablename__ = "songs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    id_artist = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    launch_date = db.Column(db.Date, nullable=False)
    exp_date = db.Column(db.Date, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    duration = db.Column(db.Time, nullable=False)
    n_replays = db.Column(db.Integer, nullable=False)
    artist = db.relationship('Artist', back_populates='song', lazy=True)
    album = db.relationship('Album', secondary=songs_albums, back_populates='song', lazy=True)
    playlist = db.relationship('Playlist', secondary=songs_playlist, back_populates='song', lazy=True)


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


def album_list(id_artist):
    values = db.session.query(Album).filter_by(id_artist=id_artist).all()
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
    values = db.session.query(Song).join(songs_albums).filter_by(id_album=id_album).all()
    return values


def search_a_song(song_title):
    if song_title:
        found = db.session.query(Song.id).filter(Song.title.contains(song_title)).all()
        if operator.not_(found):
            found = db.session.query(Song.id).all()

        return found


def search_an_album(album_name):
    if album_name:
        found = db.session.query(Album.id).filter(Album.album_name.contains(album_name)).all()
        if operator.not_(found):
            found = db.session.query(Album.id).all()

        return found
