from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sys
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
from time import sleep
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.image import Image

class SpotifyPlayer(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 2
        
        # Initialize the Spotipy client with the access token
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope='user-read-playback-state,user-modify-playback-state'))
        # Set the output device to the current playing device 
        self.spID = getDeviceID()
        self.sp.start_playback(device_id=self.spID) 

        # Create buttons
        self.play_button = Button(text='',
                            size_hint=(0.1, 0.1),
                            font_size= 36)
        self.skip_button = Button(text='',
                            size_hint=(0.1, 0.1),
                            font_size= 36)
        self.back_button = Button(text='',
                            size_hint=(0.1, 0.1),
                            font_size= 36)
        
        # Create song label
        self.song_layout = GridLayout(cols=1)
        self.song = Label(text="Now Listening...",
                          size_hint = (1,1))
        self.song_layout.add_widget(self.song)
        self.add_widget(self.song_layout)
        Clock.schedule_once(self.update_song, 1)

        # Make button control panel
        self.control_layout = GridLayout(cols=3)
        self.add_widget(self.control_layout)
        
        # add buttons to control panel
        self.play_button.bind(on_press=lambda *args: self.toggle_play())
        self.play_button.background_normal = 'img/play.png'
        self.control_layout.add_widget(self.play_button, index = 1)

        self.skip_button.bind(on_press=lambda *args: self.skip_track())
        self.skip_button.background_normal = 'img/skip.png'
        self.control_layout.add_widget(self.skip_button, index = 0)

        self.back_button.bind(on_press=lambda *args: self.back_track())
        self.back_button.background_normal = 'img/back.png'
        self.control_layout.add_widget(self.back_button, index = 2)

        
    def skip_track(self):
        self.sp.next_track(device_id=self.spID)
        Clock.schedule_once(self.update_song, 1)
    
    def back_track(self):
        self.sp.previous_track(device_id=self.spID)
        Clock.schedule_once(self.update_song, 1)

    def toggle_play(self):
        if self.sp.current_playback()['is_playing']:
            self.sp.pause_playback()
            self.play_button.background_normal = 'img/pause.png'
        else:
            self.sp.start_playback(device_id=self.spID)
            self.play_button.background_normal = 'img/play.png'
            

    def get_current_song(self):
        current_playback = self.sp.current_playback()
        if current_playback is None:
            return "Now Listening..."
        song_name = current_playback['item']['name']
        artist_name = current_playback['item']['artists'][0]['name']
        return f"{song_name} - {artist_name}"

    def update_song(self, dt):
        self.song.text = self.get_current_song()

def getDeviceID():
    # Initialize the Spotipy client with the access token
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope='user-read-playback-state'))

    # Get the current playback information, which includes the device ID
    playback_info = sp.current_playback()

    # Print the device ID
    device_id = playback_info['device']['id']
    print(f"Your device ID is: {device_id}")
    return device_id


 ############## EXAMPLE FUNCTIONS #########################
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

