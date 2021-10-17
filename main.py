#!/usr/bin/python3
import playlist_cover
from blocked_entities import blocked_tracks
import random
from datetime import datetime
from pytz import timezone
import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = YOUR_CLIENT_ID,
                                               client_secret = YOUR_CLIENT_SECRET,
                                               redirect_uri= YOUR_REDIRECT_URI,
                                               scope="user-read-playback-state, user-read-private, playlist-modify-public, ugc-image-upload, playlist-modify-private, user-top-read, user-library-modify, user-library-read, user-read-currently-playing, app-remote-control, streaming",
                                               cache_path=".spotipyoauthcache"))

Repeat_Rewind = YOUR_REPEAT_REWIND_PLAYLIST_ID
Todays_Top_Hits = "37i9dQZF1DXcBWIGoYBM5M"
RapCaviar = "37i9dQZF1DX0XUsuxWHRQd"
Mega_Hit_Mix = "37i9dQZF1DXbYM3nMM0oPk"
Pop_Sauce = "37i9dQZF1DXaPCIWxzZwR1"
playlist_name = "| s p o t i . p y |"

def get_playlist_id():
    playlists_user_lib = sp.current_user_playlists(limit=50, offset=0)
    while True:
        for i in range(50):
            if playlists_user_lib["items"][i]["name"] == playlist_name:
                playlist_id = playlists_user_lib["items"][i]["id"]
                return playlist_id

def get_songs_in_playlist(playlist_id):
    song_list = []
    songs_in_playlist = sp.playlist(playlist_id, fields = None, market = None, additional_types = ('track', ))
    for song_number in range(len(songs_in_playlist["tracks"]["items"])): song_list.append(songs_in_playlist["tracks"]["items"][song_number]["track"]["id"])
    return song_list

def get_top_songs():
    song_list = []
    top_songs = sp.current_user_top_tracks(limit = 30, offset = 0, time_range = 'short_term')
    for song_number in range(len(top_songs["items"])): song_list.append(top_songs["items"][song_number]["id"])
    return song_list

def get_liked_songs(limit):
    song_list = []
    liked_songs = sp.current_user_saved_tracks(limit, offset = 0, market = None)
    for song_number in range(len(liked_songs["items"])): song_list.append(liked_songs["items"][song_number]["track"]["id"])
    return song_list

def get_songs_from_playlist(playlist_id):
    song_list = []
    songs_in_playlist = sp.playlist(playlist_id, fields = None, market = None, additional_types = ('track', ))
    for song_number in range(20):
        try: song_list.append(songs_in_playlist["tracks"]["items"][song_number]["track"]["id"])
        except: print("!Error on", get_time("%d.%m.%Y at %H:%M %Z."), "[Track #" + str(song_number + 1), "in", songs_in_playlist["name"] + "]")
    return song_list

def add_songs(playlist_id):
    list_songs1 = get_top_songs()
    list_songs2 = get_liked_songs(30)
    list_songs4 = get_songs_from_playlist(Repeat_Rewind)
    list_songs3 = get_songs_from_playlist(Todays_Top_Hits)
    list_songs5 = get_songs_from_playlist(RapCaviar)
    list_songs6 = get_songs_from_playlist(Mega_Hit_Mix)
    list_songs7 = get_songs_from_playlist(Pop_Sauce)
    print("!Fetching songs.")
    songs_add = list(set(list_songs1 + list_songs2 + list_songs3 + list_songs4 + list_songs5 + list_songs6 + list_songs7))
    songs_add = check_blocked_entity(songs_add, blocked_tracks)
    random.shuffle(songs_add)
    songs_add = reorder_top_songs(songs_add)
    del songs_add[100:]
    sp.playlist_add_items(playlist_id, songs_add, position = None)
    print("!Songs added.")

def check_blocked_entity(songs_add, blocked_tracks):
    blocked_tracks_found = list(set(songs_add) & set(blocked_tracks))
    for i in range(len(blocked_tracks_found)):
        songs_add.remove(blocked_tracks_found[i])
        track = sp.track(blocked_tracks_found[i], market = None)
        title = track["name"]
        artist = track["artists"][0]["name"]
        print("!Song", title, "by", artist, "was not added. [Track ID blocked]")
    return songs_add

def reorder_top_songs(songs_add):
    for track_id in get_liked_songs(10)[::-1]:
        if track_id in songs_add:
            songs_add.remove(track_id)
            songs_add.insert(0, track_id)
    return songs_add

def get_time(format):
    now_time = datetime.now(timezone('Europe/Berlin'))
    date_time = now_time.strftime(format)
    return date_time

def listening_activity(user_name):
    try:
        track_id = sp.current_user_playing_track()["item"]["id"]
        track = sp.track(track_id, market = None)
        artists = []
        separator = ", "
        for i in range(len(track["artists"])): artists.append(track["artists"][i]["name"])
        if len(artists) == 2: separator = " and "
        artists = separator.join(artists)
        activity_status = str(user_name + " is currently listening to " + track["name"] + " by " + artists)
    except: activity_status = str(user_name + " is offline")
    return activity_status

def create_playlist(user_id, desc):
    sp.user_playlist_create(user_id, playlist_name, public = True, collaborative = False, description = desc)
    print("!New playlist added.")
    playlist_id = get_playlist_id()
    sp.playlist_upload_cover_image(playlist_id, playlist_cover.cover)
    print("!Cover image updated...")
    add_songs(playlist_id)
    print("!Playlist sucessfully created.")
    return playlist_id

def refresh_playlist(playlist_id, desc):
    sp.playlist_remove_all_occurrences_of_items(playlist_id, get_songs_in_playlist(playlist_id), snapshot_id = None)
    sp.playlist_change_details(playlist_id, name = None, public = True, collaborative = None, description = desc)
    add_songs(playlist_id)
    print("!Playlist refreshed successfully.")

def main():
    user = sp.current_user()
    user_name = user["display_name"]
    user_id = user["id"]
    desc = str(listening_activity(user_name) + ". This playlist was auto-generated. Last updated on " + get_time("%d.%m.%Y at %H:%M %Z."))
    try: playlist_id = get_playlist_id()
    except: playlist_id = create_playlist(user_id, desc)
    if sp.playlist(playlist_id, fields=None, market=None, additional_types=('track', ))["description"] == "clear" or get_time("%H:%M") == "20:00": refresh_playlist(playlist_id, desc)
    sp.playlist_change_details(playlist_id, name = None, public = True, collaborative = None, description = desc)
    print("!System running.")

main()
