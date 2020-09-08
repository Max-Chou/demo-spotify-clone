import os
import click
from flask.cli import AppGroup
from flask_migrate import Migrate
from app import create_app
from app.extensions import db
from app.models import User, Song, Genre, Album, Artist, Playlist, PlaylistSong
from datetime import timedelta

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

genre_cli = AppGroup('genre')
album_cli = AppGroup('album')
artist_cli = AppGroup('artist')

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Song=Song, Genre=Genre, Artist=Artist,
                Album=Album, Playlist=Playlist, PlaylistSong=PlaylistSong)



@genre_cli.command('create')
@click.option('--name', prompt='The Genre: ')
def create_genre(name):
    genre = Genre.query.filter_by(name=name).first()
    if genre is None:
        genre = Genre(name=name)
        db.session.add(genre)
        db.session.commit()
        click.echo("The genre {} has been created!".format(name))
    else:
        click.echo("The genre {} was used!".format(name))


@artist_cli.command('create')
@click.option('--name', prompt='The Artist: ')
def create_artist(name):
    artist = Artist.query.filter_by(name=name).first()
    if artist is None:
        artist = Artist(name=name)
        db.session.add(artist)
        db.session.commit()
        click.echo("The artist {} has been created!".format(name))
    else:
        click.echo("The artist {} was used!".format(name))


# create initial tables for test!
@app.cli.command("init")
def init():

    # create artists
    artists = [
        'Mickey Mouse',
        'Goofy',
        'Bart Simpson',
        'Homer',
        'Bruce Lee',
    ]

    for name in artists:
        artist = Artist.query.filter_by(name=name).first()
        if artist is None:
            artist = Artist(name=name)
        db.session.add(artist)
    
    try:
        db.session.commit()
    except:
        db.session.rollback()

    # create genre
    genres = [
        'Rock',
        'Pop',
        'Hip-hop',
        'Rap',
        'R & R',
        'Classical',
        'Techno',
        'Jazz',
        'Folk',
        'Country',
    ]

    for name in genres:
        genre = Genre.query.filter_by(name=name).first()
        if genre is None:
            genre = Genre(name=name)
        db.session.add(genre)
    
    try:
        db.session.commit()
    except:
        db.session.rollback()

    # create albums
    albums = [
        ('Becon and Eggs', 2, 4, '/shutify/app/static/images/artwork/clearday.jpg', '/static/images/artwork/clearday.jpg'),
        ('Pizza head', 5, 10, '/shutify/app/static/images/artwork/energy.jpg', '/static/images/artwork/energy.jpg'),
        ('Summer Hits', 3, 1, '/shutify/app/static/images/artwork/goinghigher.jpg', '/static/images/artwork/goinghigher.jpg'),
        ('The movie soundtrack', 2, 9, '/shutify/app/static/images/artwork/funkyelement.jpg', '/static/images/artwork/funkyelement.jpg'),
        ('Best of the Worst', 1, 3, '/shutify/app/static/images/artwork/popdance.jpg', '/static/images/artwork/popdance.jpg'),
        ('Hello World', 3, 6, '/shutify/app/static/images/artwork/ukulele.jpg', '/static/images/artwork/ukulele.jpg'),
        ('Best beats', 4, 7, '/shutify/app/static/images/artwork/sweet.jpg', '/static/images/artwork/sweet.jpg'),
    ]

    for item in albums:
        album = Album.query.filter_by(title=item[0]).first()
        if album is None:
            album = Album(
                title=item[0],
                artist_id=item[1],
                genre_id=item[2],
                artwork_path=item[3],
                artwork_url=item[4],
            )
        db.session.add(album)

    try:
        db.session.commit()
    except:
        db.session.rollback()

    # songs

    songs = [
        ('Acoustic Breeze', 1, 5, 8, timedelta(minutes=2, seconds=37), '/shutify/app/static/music/bensound-acousticbreeze.mp3', '/static/music/bensound-acousticbreeze.mp3', 1, 10),
        ('A new beginning', 1, 5, 1, timedelta(minutes=2, seconds=35), '/shutify/app/static/music/bensound-anewbeginning.mp3', '/static/music/bensound-anewbeginning.mp3', 2, 4),
        ('Better Days', 1, 5, 2, timedelta(minutes=2, seconds=33), '/shutify/app/static/music/bensound-betterdays.mp3', '/static/music/bensound-betterdays.mp3', 3, 10),
        ('Buddy', 1, 5, 3, timedelta(minutes=2, seconds=2), '/shutify/app/static/music/bensound-buddy.mp3', '/static/music/bensound-buddy.mp3', 4, 13),
        ('Clear Day', 1, 5, 4, timedelta(minutes=1, seconds=29), '/shutify/app/static/music/bensound-clearday.mp3', '/static/music/bensound-clearday.mp3', 5, 8),
        ('Going Higher', 2, 1, 1, timedelta(minutes=4, seconds=4), '/shutify/app/static/music/bensound-goinghigher.mp3', '/static/music/bensound-goinghigher.mp3', 1, 34),
        ('Funny Song', 2, 4, 2, timedelta(minutes=3, seconds=7), '/shutify/app/static/music/bensound-funnysong.mp3', '/static/music/bensound-funnysong.mp3', 2, 12),
        ('Funky Element', 2, 1, 3, timedelta(minutes=3, seconds=8), '/shutify/app/static/music/bensound-funkyelement.mp3', '/static/music/bensound-funkyelement.mp3', 2, 26),
        ('Extreme Action', 2, 1, 4, timedelta(minutes=8, seconds=3), '/shutify/app/static/music/bensound-extremeaction.mp3', '/static/music/bensound-extremeaction.mp3', 3, 29),
        ('Epic', 2, 4, 5, timedelta(minutes=2, seconds=58), '/shutify/app/static/music/bensound-epic.mp3', '/static/music/bensound-epic.mp3', 3, 17),
        ('Energy', 2, 1, 6, timedelta(minutes=2, seconds=59), '/shutify/app/static/music/bensound-energy.mp3', '/static/music/bensound-energy.mp3', 4, 26),
        ('Dubstep', 2, 1, 7, timedelta(minutes=2, seconds=3), '/shutify/app/static/music/bensound-dubstep.mp3', '/static/music/bensound-dubstep.mp3', 5, 22),
        ('Happiness', 3, 6, 8, timedelta(minutes=4, seconds=21), '/shutify/app/static/music/bensound-happiness.mp3', '/static/music/bensound-happiness.mp3', 5, 3),
        ('Happy Rock', 3, 6, 9, timedelta(minutes=1, seconds=45), '/shutify/app/static/music/bensound-happyrock.mp3', '/static/music/bensound-happyrock.mp3', 4, 8),
        ('Jazzy Frenchy', 3, 6, 10, timedelta(minutes=1, seconds=44), '/shutify/app/static/music/bensound-jazzyfrenchy.mp3', '/static/music/bensound-jazzyfrenchy.mp3', 3, 11),
        ('Little Idea', 3, 6, 1, timedelta(minutes=2, seconds=49), '/shutify/app/static/music/bensound-littleidea.mp3', '/static/music/bensound-littleidea.mp3', 2, 12),
        ('Memories', 3, 6, 2, timedelta(minutes=3, seconds=50), '/shutify/app/static/music/bensound-memories.mp3', '/static/music/bensound-memories.mp3', 1, 6),
        ('Moose', 4, 7, 1, timedelta(minutes=2, seconds=43), '/shutify/app/static/music/bensound-moose.mp3', '/static/music/bensound-moose.mp3', 5, 2),
        ('November', 4, 7, 2, timedelta(minutes=3, seconds=32), '/shutify/app/static/music/bensound-november.mp3', '/static/music/bensound-november.mp3', 4, 5),
        ('Of Elias Dream', 4, 7, 3, timedelta(minutes=4, seconds=58), '/shutify/app/static/music/bensound-ofeliasdream.mp3', '/static/music/bensound-ofeliasdream.mp3', 3, 5),
        ('Pop Dance', 4, 7, 2, timedelta(minutes=2, seconds=42), '/shutify/app/static/music/bensound-popdance.mp3', '/static/music/bensound-popdance.mp3', 2, 11),
        ('Retro Soul', 4, 7, 5, timedelta(minutes=3, seconds=36), '/shutify/app/static/music/bensound-retrosoul.mp3', '/static/music/bensound-retrosoul.mp3', 1, 11),
        ('Sad Day', 5, 2, 1, timedelta(minutes=2, seconds=28), '/shutify/app/static/music/bensound-sadday.mp3', '/static/music/bensound-sadday.mp3', 1, 9),
        ('Sci-fi', 5, 2, 2, timedelta(minutes=4, seconds=44), '/shutify/app/static/music/bensound-scifi.mp3', '/static/music/bensound-scifi.mp3', 2, 9),
        ('Slow Motion', 5, 2, 3, timedelta(minutes=3, seconds=26), '/shutify/app/static/music/bensound-slowmotion.mp3', '/static/music/bensound-slowmotion.mp3', 3, 4),
        ('Sunny', 5, 2, 4, timedelta(minutes=2, seconds=20), '/shutify/app/static/music/bensound-sunny.mp3',  '/static/music/bensound-sunny.mp3', 4, 19),
        ('Sweet', 5, 2, 5, timedelta(minutes=5, seconds=7), '/shutify/app/static/music/bensound-sweet.mp3', '/static/music/bensound-sweet.mp3', 5, 17),
        ('Tenderness ', 3, 3, 7, timedelta(minutes=2, seconds=3), '/shutify/app/static/music/bensound-tenderness.mp3', '/static/music/bensound-tenderness.mp3', 4, 13),
        ('The Lounge', 3, 3, 8, timedelta(minutes=4, seconds=16), '/shutify/app/static/music/bensound-thelounge.mp3', '/static/music/bensound-thelounge.mp3', 3, 7),
        ('Ukulele', 3, 3, 9, timedelta(minutes=2, seconds=26), '/shutify/app/static/music/bensound-ukulele.mp3', '/static/music/bensound-ukulele.mp3', 2, 22),
        ('Tomorrow', 3, 3, 1, timedelta(minutes=4, seconds=54), '/shutify/app/static/music/bensound-tomorrow.mp3 ', '/static/music/bensound-tomorrow.mp3', 1, 15),
    ]

    for item in songs:
        song = Song.query.filter_by(title=item[0]).first()
        if song is None:
            song = Song(
                title=item[0],
                artist_id=item[1],
                album_id=item[2],
                genre_id=item[3],
                duration=item[4],
                file_path=item[5],
                file_url=item[6],
                track=item[7],
                num_plays=item[8],
            )

        db.session.add(song)

    try:
        db.session.commit()
    except:
        db.session.rollback()
