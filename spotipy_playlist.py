from datetime import datetime
import time
import random
from playlistcover import playlist_cover
import spotipy
from spotipy.oauth2 import SpotifyOAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="YOUR_CLIENT_ID",
                                               client_secret="YOUR_CLIENT_SECRET",
                                               redirect_uri="YOUR_REDIRECT_URI",
                                               scope="user-read-playback-state, user-read-private, playlist-modify-public, ugc-image-upload, playlist-modify-private, user-top-read, user-library-modify, user-library-read, user-read-currently-playing"))
                                               
def get_top_songs():
    list_of_top_songs = []
    top_songs = sp.current_user_top_tracks(limit=30, offset=0, time_range='short_term')
    for i in range(len(top_songs["items"])):
        list_of_top_songs.append(top_songs["items"][i]["id"])
    return list_of_top_songs

def get_playlist_id():
    list_of_playlists = sp.current_user_playlists(limit=50, offset=0)
    z, i = 1, -1
    while z:
        i += 1
        if list_of_playlists["items"][i]["name"] == "| r a n d o m . p y |":
            playlist_id = list_of_playlists["items"][i]["id"]
            break
        else:
            continue
    return playlist_id

def get_songs_in_playlist(playlist_id): 
    list_songs_in_playlist = []
    songs_in_playlist = sp.playlist(playlist_id, fields=None, market=None, additional_types=('track', ))
    for i in range(len(songs_in_playlist["tracks"]["items"])):
        list_songs_in_playlist.append(songs_in_playlist["tracks"]["items"][i]["track"]["id"])
    return list_songs_in_playlist

def get_songs_from_spotify_playlist(playlist_id):
    list_songs_spotify = []
    songs_in_playlist = sp.playlist(playlist_id, fields=None, market=None, additional_types=('track', ))
    for i in range(14):
        list_songs_spotify.append(songs_in_playlist["tracks"]["items"][i]["track"]["id"])
    return list_songs_spotify

def get_liked_songs():
    list_liked_songs = []
    for i in range(len(sp.current_user_saved_tracks(limit=40, offset=0, market=None)["items"])):
        list_liked_songs.append(sp.current_user_saved_tracks(limit=40, offset=0, market=None)["items"][i]["track"]["id"])
    return list_liked_songs

def check_if_songs_already_added(list_songs_in_playlist,songs_to_add):
    for x in list_songs_in_playlist:
        for y in songs_to_add:
            if x == y:
                songs_to_add.remove(x)
    return songs_to_add

def add_songs(Repeat_Rewind_id,playlist_id):
    list_top_songs = check_if_songs_already_added(get_songs_in_playlist(playlist_id), get_top_songs())
    list_Todays_Top_Hits = check_if_songs_already_added(get_songs_in_playlist(playlist_id), get_songs_from_spotify_playlist("37i9dQZF1DXcBWIGoYBM5M"))
    list_Repeat_Rewind = check_if_songs_already_added(get_songs_in_playlist(playlist_id), get_songs_from_spotify_playlist(Repeat_Rewind_id))
    list_RapCaviar = check_if_songs_already_added(get_songs_in_playlist(playlist_id), get_songs_from_spotify_playlist("37i9dQZF1DX0XUsuxWHRQd"))
    list_Mega_Hit_Mix = check_if_songs_already_added(get_songs_in_playlist(playlist_id), get_songs_from_spotify_playlist("37i9dQZF1DXbYM3nMM0oPk"))
    list_liked_songs = check_if_songs_already_added(get_songs_in_playlist(playlist_id),get_liked_songs())
    print("Fetching songs...")

    list_songs_to_add = list(set(list_top_songs + list_Todays_Top_Hits + list_Repeat_Rewind + list_RapCaviar + list_Mega_Hit_Mix + list_liked_songs))
    random.shuffle(list_songs_to_add)
    del list_songs_to_add[100:]

    if list_songs_to_add != []:
        sp.playlist_add_items(playlist_id, list_songs_to_add, position=None)
        print("Songs added.")

def loop():
    Repeat_Rewind_id ="YOUR_REPEAT_REWIND_PLAYLIST_ID"
    user = sp.current_user()
    user_name = user["display_name"]
    user_id = user["id"]

    try:
        crtly = sp.current_user_playing_track()
        song = crtly["item"]["name"]
        link = crtly["item"]["external_urls"]["spotify"]
        artist = crtly["item"]["album"]["artists"][0]["name"]
        activity_status = str(user_name + " is currently listening to " + song + " by " + artist)
    except:
        activity_status = str(user_name +" is offline")
        
    current_date_time = datetime.today().strftime('%m/%d/%Y at %H:%M.')
    desc = str(activity_status + ". This playlist was auto-generated. Last updated on " + current_date_time)

    try:
        playlist_id = get_playlist_id()
    except:
        sp.user_playlist_create(user_id, "| r a n d o m . p y |", public=True, collaborative=False, description=desc)
        print("New playlist added...")
        playlist_id = get_playlist_id()
        sp.playlist_upload_cover_image(playlist_id, playlist_cover)
        print("Cover image updated...")
        add_songs(Repeat_Rewind_id,playlist_id)
        print("Playlist sucessfully created!")

    if "clear" == sp.playlist(playlist_id, fields=None, market=None, additional_types=('track', ))["description"]:
        sp.playlist_remove_all_occurrences_of_items(playlist_id, get_songs_in_playlist(playlist_id), snapshot_id=None)
        sp.playlist_change_details(playlist_id, name=None, public=True, collaborative=None, description=desc)
        add_songs(Repeat_Rewind_id,playlist_id)
        sp.playlist_upload_cover_image(playlist_id, playlist_cover)
        print("Playlist was cleared and refilled.")
    else:
        if datetime.today().strftime('%H:%M') == "20:00" or datetime.today().strftime('%H:%M') == "20:01":
            sp.playlist_upload_cover_image(playlist_id, playlist_cover)
            sp.playlist_remove_all_occurrences_of_items(playlist_id, get_songs_in_playlist(playlist_id), snapshot_id=None)
            add_songs(Repeat_Rewind_id,playlist_id)
            print("Playlist updated.")
        sp.playlist_change_details(playlist_id, name=None, public=True, collaborative=None, description=desc)

while True:
    loop()
    time.sleep(60)
