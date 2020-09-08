from flask import render_template, redirect, url_for, request, abort, jsonify
from . import page
from ..extensions import db
from ..models import User, Artist, Album, Genre, Song, Playlist, PlaylistSong
from .forms import SigninForm, SignupForm
from flask_login import login_required, current_user, logout_user, login_user


@page.route('/')
def index():

    songs = Song.query.all()

    data = [song.id for song in songs]

    return render_template('index.html', data=data)


@page.route('/search')
def search():

    if request.args.get('term'):

        term = "{}%".format(request.args.get('term'))

        songs = Song.query.filter(Song.title.ilike(term)).all()

        data = [song.id for song in songs]

        artists = Artist.query.filter(Artist.name.ilike(term)).all()

        albums = Album.query.filter(Album.title.ilike(term)).all()

        return render_template('search.html', songs=songs, artists=artists, albums=albums, term=request.args.get('term'), data=data)
            

    return render_template('search.html', data=None)


@page.route('/album')
def album():

    if request.args.get('id'):
        album = Album.query.get_or_404(request.args.get('id'))

        data = [song.id for song in album.songs.all() ]

        return render_template('album.html', album=album, data=data)
    else:
        return abort(404)


@page.route('/artist')
def artist():

    if request.args.get('id'):
        artist = Artist.query.get_or_404(request.args.get('id'))

        data = [song.id for song in artist.songs.all() ]

        return render_template('artist.html', artist=artist, data=data)
    else:
        return abort(404)


@page.route('/browse')
def browse():
    albums = Album.query.all()
    return render_template('browse.html', albums=albums, data=None)


@page.route('/playlist')
def playlist():
    return "<h1>Playlist Page</h1>"


@page.route('/register', methods=['GET', 'POST'])
def register():

    signupForm = SignupForm()

    if signupForm.validate_on_submit():
        user = User(
            username=signupForm.username.data,
            first_name=signupForm.first_name.data,
            last_name=signupForm.last_name.data,
            email=signupForm.email.data,
            password=signupForm.password.data
        )

        try:
            db.session.add(user)
            db.session.commit()
            redirect(url_for('page.login'))
        except:
            db.session.rollback()

    return render_template('register.html', signupForm=signupForm)


@page.route('/login', methods=['GET', 'POST'])
def login():
    signinForm = SigninForm()

    if signinForm.validate_on_submit():
        user = User.query.filter_by(username=signinForm.username.data).first()
        if user and user.verify_password(signinForm.password.data):
            login_user(user)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('page.index')
            return redirect(next)
    
    return render_template('login.html', signinForm=signinForm)


@page.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('page.index'))


@page.route('/settings')
def settings():
    return "<h1>Settings Page</h1>"


@page.route('/updateDetails')
def updateDetails():
    return "<h1>updateDetails Page</h1>"


@page.route('/yourMusic')
def yourMusic():
    return "<h1>yourMusic Page</h1>"


@page.route('/getSongJson', methods=['POST'])
def getSongJson():

    if request.form.get('songId'):
        song = Song.query.get_or_404(request.form.get('songId'))

        result = {
            'id': song.id,
            'title': song.title,
            'artist': song.artist_id,
            'album': song.album_id,
            'path': song.file_url
        }

        return jsonify(result)

    else:
        return abort(404)    


@page.route('/getArtistJson', methods=['POST'])
def getArtistJson():

    if request.form.get('artistId'):
        artist = Artist.query.get_or_404(request.form.get('artistId'))

        result = {
            'name': artist.name,
            'id': artist.id,
        }

        return jsonify(result)

    else:
        return abort(404)    


@page.route('/getAlbumJson', methods=['POST'])
def getAlbumJson():

    if request.form.get('albumId'):
        album = Album.query.get_or_404(request.form.get('albumId'))

        result = {
            'id': album.id,
            'artworkPath': album.artwork_url,
        }

        return jsonify(result)

    else:
        return abort(404)    


@page.route('/updatePlays', methods=['POST'])
def updatePlays():


    if request.form.get('songId'):
        song = Song.query.get_or_404(request.form.get('songId'))

        song.num_plays += 1
        db.session.add(song)
        db.session.commit()
        return jsonify({'success':True}), 200, {'ContentType':'application/json'} 
    else:
        return abort(404)

# for admin only
@page.route('/uploads')
def uploads():
    return "<h1>Uploads Page</h1>"
