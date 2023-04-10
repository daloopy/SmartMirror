from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sys
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
from time import sleep
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button


class SpotifyPlayer(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        laptopID = "11d9bf2ca1e98be4eafafcf94df81143796be422"

        # Initialize the Spotipy client with the access token
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope='user-read-playback-state,user-modify-playback-state'))

        # Set the output device to your device ID
        sp.start_playback(device_id=laptopID) 

        # Create a button to toggle the playback state
        play_button = Button(text='Play',
                             size_hint=(0.1, 0.1),
                             pos_hint={"right":1, "top": 0},
                             font_size= 36)
        
        play_button.bind(on_press=lambda *args: sp.pause_playback() if sp.current_playback()['is_playing'] else sp.start_playback(device_id=laptopID))
        self.add_widget(play_button)

def searchSpotify(search_str = 'Radiohead'):
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    result = sp.search(search_str)
    return result

def showResults(result):
    pprint(result)

def listBirdy():
    birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    results = spotify.artist_albums(birdy_uri, album_type='album')
    albums = results['items']
    while results['next']:
        results = spotify.next(results)
        albums.extend(results['items'])

    for album in albums:
        print(album['name'])

def playSpotify():
    scope = "user-read-playback-state,user-modify-playback-state"
    sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))

    # Shows playing devices
    res = sp.devices()
    pprint(res)

    # Change track
    sp.start_playback(uris=['spotify:track:6gdLoMygLsgktydTQ71b15'])

    # Change volume
    sp.volume(100)
    sleep(2)
    sp.volume(50)
    sleep(2)
    sp.volume(100)

def listSavedSongs():
    scope = "user-library-read"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    results = sp.current_user_saved_tracks()
    for idx, item in enumerate(results['items']):
        track = item['track']
        print(idx, track['artists'][0]['name'], " – ", track['name'])   

def getDeviceID():
    # Initialize the Spotipy client with the access token
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope='user-read-playback-state'))

    # Get the current playback information, which includes the device ID
    playback_info = sp.current_playback()

    # Print the device ID
    device_id = playback_info['device']['id']
    print(f"Your device ID is: {device_id}")



# laptop: 11d9bf2ca1e98be4eafafcf94df81143796be422