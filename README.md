# demo-spotify-clone
Spotify-like app

This app offers some main features like Spotify. 

## Features

* Available:
    * Users can create their playlists.
    * Users can listen the songs on the platform.
    * Users can search the song by artist's name, album's title and song's title.

The music player is not perfect. And there are some features broken.

## Demo

I host the app on my own server. [Shutify](https://shutify.afai97202013.com)

The available accounts for the demo:

| Username | Password      |
|----------|---------------|
| John     | 12345678      |

## Requirements

* Simple 
    * Docker Engine
    * Docker Compose


* Tradition
    * Python
    * Flask
    * Flask-SQLAlchemy
    * Flask-WTF
    * Flask-Login
    * SQL Database
    * WSGI Server (Optional)
    * Web Server (Optional)


## Usage

0. Copy the `env.example` to `.env`, which contains the environment variables for this app.

1. Clone this repo to your computer and run `docker-compose up --build` to create a image and launch the whole containers.

2. Run `docker-compose exec faketube flask db upgrade` to migrate the database.

3. And open your browser, then visit `localhost:8000`.

### TODO

* Feature:
    * Add an admin dashboard to manage songs on the platform.
    * let users cancel their accounts.


* System:
    * Deploy on Clouds, AWS or GCP.
    * Since the app has many static contents, videos and pictures, the CDN and file storage system are required.
    * Divide the app into Frontend and Backend. Sever-side rendering, Jinga, is not well for scaling and I don't like the frontend works.


* Docker:
    * Deploy on Docker Swarm and Kubernetes.
