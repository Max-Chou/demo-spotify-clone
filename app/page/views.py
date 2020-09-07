from flask import render_template, redirect, url_for, request
from . import page


@page.route('/')
def index():
    return "<h1>Hello, World!</h1>"


@page.route('/search')
def search():
    return "<h1>Search Page</h1>"


@page.route('/album')
def album():
    return "<h1>Album Page</h1>"


@page.route('/artist')
def artist():
    return "<h1>Artist Page</h1>"


@page.route('/browse')
def browse():
    return "<h1>Browse Page</h1>"


@page.route('/playlist')
def playlist():
    return "<h1>Playlist Page</h1>"


@page.route('/register')
def register():
    return "<h1>Register Page</h1>"


@page.route('/settings')
def settings():
    return "<h1>Settings Page</h1>"


@page.route('/updateDetails')
def updateDetails():
    return "<h1>updateDetails Page</h1>"


@page.route('/yourMusic')
def yourMusic():
    return "<h1>yourMusic Page</h1>"


# for admin only
@page.route('/uploads')
def uploads():
    return "<h1>Uploads Page</h1>"
