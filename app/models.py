from .extensions import db, login_manager
from flask_login import UserMixin
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    picture_url = db.Column(db.String(255))
    picture_path = db.Column(db.String(255))

    playlists = db.relationship('Playlist', backref='user', lazy='dynamic')


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    albums = db.relationship('Album', backref='artist', lazy='dynamic')
    songs = db.relationship('Song', backref='artist', lazy='dynamic')



class Genre(db.Model):
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    albums = db.relationship('Album', backref='genre', lazy='dynamic')
    songs = db.relationship('Song', backref='genre', lazy='dynamic')


class Album(db.Model):
    __tablename__ = 'albums'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    artwork_path = db.Column(db.String(255))
    artwork_url = db.Column(db.String(255))

    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'))
    
    songs = db.relationship('Song', backref='album', lazy='dynamic')


class Song(db.Model):
    __tablename__ = 'songs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Interval, default=timedelta())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    track = db.Column(db.Integer)
    num_plays = db.Column(db.Integer, default=0)
    file_path = db.Column(db.String(255))
    file_url = db.Column(db.String(255))

    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'))
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'))


class Playlist(db.Model):
    __tablename__ = 'playlists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    songs = db.relationship('PlaylistSong', backref='playlist', lazy="joined")


class PlaylistSong(db.Model):
    __tablename__ = 'playlistsongs'

    id = db.Column(db.Integer, primary_key=True)
    track = db.Column(db.Integer, unique=True)
    
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'))
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'))
