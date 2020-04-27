# Lyricspy

## Pre-requisites

pipenv and pipenv-shebang:

```
$ pip install --user pipenv
$ pip install --user pipenv-shebang
```

## Installation

Make sure you have the pre-requisites then:

```
$ git clone https://github.com/cvaldev/lyricspy.git
$ cd lyricspy
$ pipenv install
```

## How to use it

If you want to get the lyrics for what's currently playing on Spotify, simply run:

```
$ ./lyricspy.py
```

Alternatively you can search for a specific song by passing the artist and song like this:

```
$ ./lyricspy.py --artist artist name --song my favorite song
```
