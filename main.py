#!/usr/bin/python3
from data import *
import time
import random
from datetime import datetime
from pytz import timezone
import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope="user-read-playback-state, user-read-private, playlist-modify-public, ugc-image-upload, playlist-modify-private, user-top-read, user-library-modify, user-library-read, user-read-currently-playing, app-remote-control, streaming",
                                               cache_path=".spotipyoauthcache"))
playlist_name = "| s p o t i . p y |"

def get_playlist_id():
    playlists_user_lib = sp.current_user_playlists(limit=50, offset=0)
    for i, v in enumerate(playlists_user_lib["items"]):
        if v["name"] == playlist_name: return v["id"]

def get_songs_in_playlist(playlist_id):
    track_list = []
    tracks_in_playlist = sp.playlist(playlist_id, fields=None, market=None, additional_types=('track', ))
    for i, v in enumerate(tracks_in_playlist["tracks"]["items"]): track_list.append(v["track"]["id"])
    return track_list

def get_top_songs():
    track_list = []
    top_songs = sp.current_user_top_tracks(limit=30, offset=0, time_range='short_term')
    for i, v in enumerate(top_songs["items"]): track_list.append(v["id"])
    return track_list

def get_liked_songs(limit):
    track_list = []
    liked_songs = sp.current_user_saved_tracks(limit, offset=0, market=None)
    for i, v in enumerate(liked_songs["items"]): track_list.append(v["track"]["id"])
    return track_list

def get_songs_from_playlist(playlist_id):
    track_list = []
    songs_in_playlist = sp.playlist(playlist_id, fields=None, market=None, additional_types=('track', ))
    for song_number in range(20):
        try: track_list.append(songs_in_playlist["tracks"]["items"][song_number]["track"]["id"])
        except: print(f"!{get_time('[%Y-%m-%d %H:%M %Z]')} Track #{str(song_number+1)} in {songs_in_playlist['name']}")
    return track_list

def check_blocked_entity(songs_add):
    blocked_tracks_found = list(set(songs_add) & set(blocked_tracks))
    for i in blocked_tracks_found:
        songs_add.remove(i)
        track = sp.track(i, market=None)
        title = track["name"]
        artist = track["artists"][0]["name"]
        print(f"!Song {title} by {artist} was not added.")
    return songs_add

def reorder_top_songs(songs_add):
    songs_add = list(set(songs_add))
    random.shuffle(songs_add)
    for i in get_liked_songs(10)[::-1]:
        if i in songs_add: songs_add.remove(i)
        songs_add.insert(0, i)
    return songs_add

def add_songs(playlist_id):
    songs_add = get_top_songs() + get_liked_songs(30)
    for i in playlist_src:
        songs_add += get_songs_from_playlist(i)
    print("!Fetching songs.")
    songs_add = check_blocked_entity(songs_add)
    songs_add = reorder_top_songs(songs_add)
    del songs_add[100:]
    sp.playlist_add_items(playlist_id, songs_add, position=None)
    print("!Songs added.")

def get_time(format):
    now_time = datetime.now(timezone('Europe/Berlin'))
    date_time = now_time.strftime(format)
    return date_time

def devices():
    devices_available = sp.devices()
    for i, v in enumerate(devices_available["devices"]):
        if v["is_active"]:
            return v["name"], v["type"]

def listening_activity(user_name):
    try:
        track_id = sp.current_user_playing_track()["item"]["id"]
        device_name, device_type = devices()
        track = sp.track(track_id, market=None)
        artists = []
        artists = [v["name"] for i, v in enumerate(track["artists"])]
        if len(artists) == 2: separator = " and "
        else: separator = ", "
        artists = separator.join(artists)
        return f"{user_name} is currently listening to {track['name']} by {artists} on {device_name} ({device_type})"
    except: return f"{user_name} is offline"

def create_playlist(user_id, desc):
    sp.user_playlist_create(user_id, playlist_name, public=True, collaborative=False, description=desc)
    print("!New playlist added.")
    playlist_id = get_playlist_id()
    add_songs(playlist_id)
    print("!Playlist sucessfully created.")
    return playlist_id

def refresh_playlist(playlist_id, desc):
    sp.playlist_remove_all_occurrences_of_items(playlist_id, get_songs_in_playlist(playlist_id), snapshot_id=None)
    sp.playlist_change_details(playlist_id, name=None, public=True, collaborative=None, description=desc)
    add_songs(playlist_id)
    print("!Playlist refreshed successfully.")

def main():
    user = sp.current_user()
    user_name = user["display_name"]
    user_id = user["id"]
    desc = str(listening_activity(user_name) + ". Last updated on " + get_time("%d.%m.%Y at %H:%M %Z."))
    playlist_id = get_playlist_id()
    if playlist_id == None: playlist_id = create_playlist(user_id, desc)
    if sp.playlist(playlist_id, fields=None, market=None, additional_types=('track', ))["description"] == "clear" or get_time("%H:%M") == "20:00": refresh_playlist(playlist_id, desc)
    sp.playlist_change_details(playlist_id, name=None, public=True, collaborative=None, description=desc)

main()
