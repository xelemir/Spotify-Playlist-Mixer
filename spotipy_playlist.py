from playlist_cover import playlist_cover
from blocked_entities import blocked_artists, blocked_tracks_id

import random
import time
from datetime import datetime
from pytz import timezone
import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="<YOUR_CLIENT_ID>",
                                               client_secret="<YOUR_CLIENT_SECRET>",
                                               redirect_uri="<YOUR_REDIRECT_URI>",
                                               scope="user-read-playback-state, user-read-private, playlist-modify-public, ugc-image-upload, playlist-modify-private, user-top-read, user-library-modify, user-library-read, user-read-currently-playing, user-read-playback-position"))

Repeat_Rewind ="<YOUR_PERSONAL_SPOTIFY_REPEAT_REWIND_ID>"
Todays_Top_Hits = "37i9dQZF1DXcBWIGoYBM5M"
RapCaviar = "37i9dQZF1DX0XUsuxWHRQd"
Mega_Hit_Mix = "37i9dQZF1DXbYM3nMM0oPk"
playlist_name = "| r a n d o m . p y |"

def get_top_songs():
    song_list = []
    top_songs = sp.current_user_top_tracks(limit=25, offset=0, time_range='short_term')
    for song_number in range(len(top_songs["items"])):
        song_list.append(top_songs["items"][song_number]["id"])
    return song_list

def get_playlist_id():
    playlists_user_lib = sp.current_user_playlists(limit=50, offset=0)
    while True:
        for i in range(50):
            if playlists_user_lib["items"][i]["name"] == playlist_name:
                playlist_id = playlists_user_lib["items"][i]["id"]
                return playlist_id

def get_songs_in_playlist(playlist_id):
    song_list = []
    songs_in_playlist = sp.playlist(playlist_id, fields=None, market=None, additional_types=('track', ))
    for song_number in range(len(songs_in_playlist["tracks"]["items"])):
        song_list.append(songs_in_playlist["tracks"]["items"][song_number]["track"]["id"])
    return song_list

def get_songs_from_playlist(playlist_id):
    song_list = []
    songs_in_playlist = sp.playlist(playlist_id, fields=None, market=None, additional_types=('track', ))
    for song_number in range(17):
        song_list.append(songs_in_playlist["tracks"]["items"][song_number]["track"]["id"])
    return song_list

def get_liked_songs():
    song_list = []
    liked_songs =sp.current_user_saved_tracks(limit=35, offset=0, market=None)
    for song_number in range(len(liked_songs["items"])):
        song_list.append(liked_songs["items"][song_number]["track"]["id"])
    return song_list

def check_blocked_entity(songs_add, blocked_artists, blocked_tracks):
    artists_songs_add = []
    for track_id in songs_add:
        artists_songs_add.append(sp.track(track_id, market=None)["artists"][0]["name"])
    check_blocked_artist = [s for s in artists_songs_add if any(xs in s for xs in blocked_artists)]
    for i in range(len(check_blocked_artist)):
        title = sp.track(songs_add[artists_songs_add.index(check_blocked_artist[i])-i], market=None)["name"]
        del songs_add[artists_songs_add.index(check_blocked_artist[i])-i]
        print("!Song", title, "by", check_blocked_artist[i], "was not added. [Artist blocked]")
        
    id_songs_add = []
    for track_id in songs_add:
        id_songs_add.append(sp.track(track_id, market=None)["id"])
    check_blocked_id = [s for s in id_songs_add if any(xs in s for xs in blocked_tracks)]
    for i in range(len(check_blocked_id)):
        del songs_add[id_songs_add.index(check_blocked_id[i])-i]
        title = sp.track(check_blocked_id[i], market=None)["name"]
        artist = sp.track(check_blocked_id[i], market=None)["artists"][0]["name"]
        print("!Song", title, "by", artist, "was not added. [ID blocked]")

    return songs_add

def add_songs(playlist_id):
    list_songs1 = get_top_songs()
    list_songs2 = get_liked_songs()
    list_songs4 = get_songs_from_playlist(Repeat_Rewind)
    list_songs3 = get_songs_from_playlist(Todays_Top_Hits)
    list_songs5 = get_songs_from_playlist(RapCaviar)
    list_songs6 = get_songs_from_playlist(Mega_Hit_Mix)
    print("!Fetching songs...")

    songs_add = list(set(list_songs1 + list_songs2 + list_songs3 + list_songs4 +list_songs5 + list_songs6))
    songs_add = check_blocked_entity(songs_add, blocked_artists, blocked_tracks_id)

    random.shuffle(songs_add)
    del songs_add[100:]

    if songs_add != []:
        sp.playlist_add_items(playlist_id, songs_add, position=None)
        print("!Songs added.")

def get_time(format):
    now_time = datetime.now(timezone('Europe/Berlin'))
    date_time = now_time.strftime(format)
    return date_time

def listening_activity(user_name):
    try:
        activity = sp.current_user_playing_track()
        song = activity["item"]["name"]
        artist = activity["item"]["album"]["artists"][0]["name"]
        activity_status = str(user_name + " is currently listening to " + song + " by " + artist)
    except:
        activity_status = str(user_name +" is offline")
    return activity_status

def create_playlist(user_id, desc):
    sp.user_playlist_create(user_id, playlist_name, public=True, collaborative=False, description=desc)
    print("!New playlist added...")
    playlist_id = get_playlist_id()
    sp.playlist_upload_cover_image(playlist_id, playlist_cover)
    print("!Cover image updated...")
    add_songs(playlist_id)
    print("!Playlist sucessfully created!")
    return playlist_id

def refresh_playlist(playlist_id, desc):
    sp.playlist_remove_all_occurrences_of_items(playlist_id, get_songs_in_playlist(playlist_id), snapshot_id=None)
    sp.playlist_change_details(playlist_id, name=None, public=True, collaborative=None, description=desc)
    add_songs(playlist_id)
    print("!Playlist refreshed successfully")

def main():
    user = sp.current_user()
    user_name = user["display_name"]
    user_id = user["id"]
    desc = str(listening_activity(user_name) + ". This playlist was auto-generated. Last updated on " + get_time("%d.%m.%Y at %H:%M %Z."))
    
    try:
        playlist_id = get_playlist_id()
    except:
        playlist_id = create_playlist(user_id, desc)

    if "clear" == sp.playlist(playlist_id, fields=None, market=None, additional_types=('track', ))["description"] or get_time("%H:%M") == "20:00":
        refresh_playlist(playlist_id, desc)

    sp.playlist_change_details(playlist_id, name=None, public=True, collaborative=None, description=desc)
    print("!System running.")

while True:
    main()
    time.sleep(60)
