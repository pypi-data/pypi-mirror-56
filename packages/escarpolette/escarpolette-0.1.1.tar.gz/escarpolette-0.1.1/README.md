# Escarpolette

This project provides a server and clients to manage your music playlist when you are hosting a party.

It supports many sites, thanks to the awesome project [youtube-dl](https://rg3.github.io/youtube-dl/).

## Features

Server:
* add items (and play them!)
* get playlist's itmes
* runs on Android! (see [instructions](#Android))

Web client:
* there is currently no web client :(

## Dependencies

* Python 3.6
* the dependencies manager [Poetry](https://poetry.eustace.io/)
* the player [mpv](https://mpv.io)

They should be available for most of the plateforms.


## Run it

### Linux

Clone the repository, then go the folder and type:

```Shell
make init
make db-upgrade
make run
```

You can now open [localhost:5000](http://localhost:5000).
Just add a new item to get the music playing!

### Android

You will need [Termux](https://termux.com/).
Then inside Termux you can install the dependencies with:

```Shell
pkg install python python-dev clang git make
pip install poetry
```

Then follow the Linux instructions.
Note that while the project can run without wake-lock, acquiring it improve the performance (with a battery trade off).

## Todo

* server
    * empty the playlist on startup
    * bonjour / mDNS
    * votes
    * prevent adding youtube / soundcloud playlists
    * restrictions by users
    * configuration of those restrictions by an admin
* web client
    * show playing status
    * votes
    * configure restrictions:
        * max video added per user
        * max video length
    * admin access:
        * configure restrictions
        * no restrictions for him
        * force video order

Don't count on it:
* android client
* iOS client
