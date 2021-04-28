# Free Leech Sync

For all your torrent ratio needs.

```
$ export HTTP_USERNAME=tracker_username
$ export HTTP_PASSWORD=tracker_password
$ export REMOTE_HOST=my.seedbox

$ python sync 600
```

## Run in Docker

```
$ docker build -t freeleech:latest .
$ docker run  -v `pwd`/data:/app/data --env-file=`pwd`/.env freeleech:latest
```
