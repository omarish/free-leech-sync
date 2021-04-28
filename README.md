# Free Leech Sync

For all your torrent ratio needs.

First, set some envvars:

```
$ export HTTP_USERNAME=tracker_username
$ export HTTP_PASSWORD=tracker_password
$ export REMOTE_HOST=my.seedbox
```

## Default

`python sync` runs a single search and checks for latest torrents

## Full Search

`python sync --full_scan=True` does searches for every letter bigram (`aa`, `ab`, `ac`, ... `zy`, `zz`).

## Run in Docker

```
$ docker build -t freeleech:latest .
$ docker run  -v `pwd`/data:/app/data --env-file=`pwd`/.env freeleech:latest
```
