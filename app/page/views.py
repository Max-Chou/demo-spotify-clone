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

        if current_user.is_authenticated:
            playlists = Playlist.query.filter_by(user_id=current_user.id).all()
        else:
            playlists = None

        return render_template('album.html', album=album, data=data, playlists=playlists)
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
@login_required
def playlist():

    if request.args.get('id'):
        playlist = Playlist.query.get_or_404(request.args.get('id'))

        songs_query = Song.query.join(PlaylistSong).join(Playlist).filter(Playlist.id == playlist.id)

        data = [song.id for song in songs_query.all() ]

        return render_template('playlist.html', data=data, playlist=playlist, songs_query=songs_query)
    else:
        return abort(404)



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

    return render_template('settings.html', data=None)


@page.route('/updateDetails')
def updateDetails():
    return render_template('updateDetails.html', data=None)


@page.route('/yourMusic')
@login_required
def yourMusic():

    playlists = Playlist.query.filter_by(user_id=current_user.id).all()

    return render_template('yourMusic.html', data=None, playlists=playlists)


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


@page.route('/createPlaylist', methods=['POST'])
def createPlaylist():

    if request.form.get('name'):
        playlist = Playlist(name=request.form.get('name'), user_id=request.form.get('userId'))
        db.session.add(playlist)
        db.session.commit()
        # return jsonify({'success':True}), 200, {'ContentType':'application/json'} 
        return ""
    else:
        return abort(404)        


@page.route('/deletePlaylist', methods=['POST'])
def deletePlaylist():

    if request.form.get('playlistId'):
        playlist = Playlist.query.get_or_404(request.form.get('playlistId'))
        playlistsongs = PlaylistSong.query.filter_by(playlist_id=playlist.id).all()
        for playlistsong in playlistsongs:
            db.session.delete(playlistsong)
        db.session.delete(playlist)
        db.session.commit()
        return ""
    else:
        return abort(404)


@page.route('/addToPlaylist', methods=['POST'])
def addToPlaylist():

    if request.form.get('playlistId') and request.form.get('songId'):
        
        playlistsong = PlaylistSong.query.filter_by(playlist_id=request.form.get('playlistId'), song_id=request.form.get('songId')).first()

        if playlistsong is None:
            track = PlaylistSong.query.filter_by(playlist_id=request.form.get('playlistId')).count()
            track += 1
            playlistsong = PlaylistSong(playlist_id=request.form.get('playlistId'), song_id=request.form.get('songId'), track=track)
            db.session.add(playlistsong)
            db.session.commit()
        return ""
    else:
        return abort(404)


@page.route('/removeFromPlaylist', methods=['POST'])
def removeFromPlaylist():
    if request.form.get('playlistId') and request.form.get('songId'):
        playlistsong = PlaylistSong.query.filter_by(playlist_id=request.form.get('playlistId'), song_id=request.form.get('songId')).first()
        
        if playlistsong:
            db.session.delete(playlistsong)
            db.session.commit()

        return ""
    else:
        return abort(404)


@page.route('/updateEmail', methods=['POST'])
@login_required
def updateEmail():
    if request.form.get('email'):
        user = User.query.filter_by(email=request.form.get('email')).first()
        if user is None:
            user = User.query.get_or_404(current_user.id)
            user.email = request.form.get('email')
            db.session.add(user)
            db.session.commit()
            return "Update successful"
        else:
            return "Email is already in use"

    else:
        return abort(404)


@page.route('/updatePassword', methods=['POST'])
@login_required
def updatePassword():
    if request.form.get('newPassword1') == request.form.get('newPassword2'):
        user = User.query.get_or_404(current_user.id)
        if user.verify_password(request.form.get('oldPassword')):
            user.password = request.form.get('newPassword1')
            db.session.add(user)
            db.session.commit()
            return "Update successful"
        else:
            return "Your passwords is not valid"
    else:
        return "Your passwords do not match"


# for admin only
@page.route('/uploads')
def uploads():
    return "<h1>Uploads Page</h1>"
