#!/usr/bin/env pipenv-shebang

"""
Returns the lyrics for the currently playing song on the spotify app.
You can also request a specific song's lyrics by passing -a <artist> -s <song>.

Requires: 
    *pipenv
    *pipenv-shebang
"""


import sys
import argparse
import dbus
import requests
import bs4


def get_params():
    if len(sys.argv) > 1:
        # Get the song and artist from the commandline args
        parser = argparse.ArgumentParser(
            description="Gets the info about a song")
        parser.add_argument(
            "-a", "--artist", help="Name of the artist", nargs="+")
        parser.add_argument("-s", "--song", help="Name of the song", nargs="+")
        args = parser.parse_args()
        artist = " ".join(args.artist)
        song = " ".join(args.song)
    else:
        # Get the song and artist from whatever spotify is playing
        bus = dbus.SessionBus()
        spotify = bus.get_object(
            "org.mpris.MediaPlayer2.spotify", "/org/mpris/MediaPlayer2")
        spotify_properties = dbus.Interface(
            spotify, 'org.freedesktop.DBus.Properties')
        metadata = spotify_properties.Get(
            'org.mpris.MediaPlayer2.Player', 'Metadata')
        artist = ",".join(metadata.get("xesam:artist"))
        song = metadata.get("xesam:title")
    return [artist, song]


def get_lyrics(artist, song):
    # Get the lyrics for a song from any one of the services.
    title = f"Lyrics for {artist} - {song}"
    lyrics = attempt_lyrics_from_genius(artist, song)
    return f"{title}\n\n{lyrics}"


def attempt_lyrics_from_genius(artist, song):
    # request: https://genius.com/<artist>-<song>-lyrics
    # song/artist translate "-" instead of space && delete "()"
    uri = f"https://genius.com/{artist}-{song}-lyrics".translate(
        str.maketrans({" ": "-", "(": "", ")": ""}))
    res = requests.get(uri)

    if res.status_code == 200:
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        lyrics = soup.select_one("div.lyrics > p").text
        return lyrics
    else:
        return "Not found"


[artist, song] = get_params()
lyrics = get_lyrics(artist, song)
print(lyrics)
