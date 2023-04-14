from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sys
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
from time import sleep
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.image import Image
from kivymd.uix.button import *
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.icon_definitions import md_icons
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.responsivelayout import MDResponsiveLayout
import requests
from kivy.core.window import Window

class SpotifyPlayer(MDFloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Initialize the Spotipy client with the access token
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope='user-read-playback-state,user-modify-playback-state'))
        # Set the output device to the current playing device 
        self.spID = getDeviceID() # "11d9bf2ca1e98be4eafafcf94df81143796be422"
        #self.sp.transfer_playback(self.spID, force_play=True)

        # Create buttons
        self.play_button = MDFloatingActionButton(icon="play-box",
                            size_hint=(0.1, 0.1), pos=(1500,200),
                            icon_size= "72")
        self.skip_button = MDFloatingActionButton(icon='skip-forward',
                            size_hint=(0.1, 0.1), pos=(1700, 200),
                            icon_size= "72")
        self.back_button = MDFloatingActionButton(icon='skip-backward',
                            size_hint=(0.1, 0.1), pos=(1300,200),
                            icon_size= "72")
        
        # Create song label
        self.song_layout = MDFloatLayout(radius = [25,0,25,0])
        self.song = Label(text="Now Listening...",
                          size_hint = (1,1))
        self.song_layout.add_widget(self.song)
        self.add_widget(self.song_layout)
        
        
        # Create album cover image
        self.download_album_image()
        self.album_image = Image(source='image.jpg', pos = (500,200), nocache=True, size=(100,100), allow_stretch=False, keep_ratio=True)
        self.song_layout.add_widget(self.album_image)
        Clock.schedule_once(self.update_song, 1)
        
        # Make button control panel
        self.control_layout = MDFloatLayout(radius = [25,25,0,0])
        self.add_widget(self.control_layout)
        
        # add buttons to control panel
        self.play_button.bind(on_press=lambda *args: self.toggle_play())
        self.control_layout.add_widget(self.play_button, index = 1)

        self.skip_button.bind(on_press=lambda *args: self.skip_track())
        self.control_layout.add_widget(self.skip_button, index = 0)

        self.back_button.bind(on_press=lambda *args: self.back_track())
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
            self.play_button.background_normal = 'img/play.png'
        else:
            self.sp.start_playback(device_id=self.spID)
            self.play_button.background_normal = 'img/pause.png'
            

    def get_current_song(self):
        current_playback = self.sp.current_playback()
        if current_playback is None:
            return "Now Listening..."
        song_name = current_playback['item']['name']
        artist_name = current_playback['item']['artists'][0]['name']
        return f"{song_name} - {artist_name}"

    def update_song(self, dt):
        self.song.text = self.get_current_song()
        self.download_album_image()
        self.update_image()
        
    def update_image(self):
        self.album_image.reload()
        
    def get_album_image(self):
        current_playback = self.sp.current_playback()
        album_cover_url = current_playback['item']['album']['images'][0]['url']
        nocache_url = album_cover_url + "?cache={cache_buster}" + "&size=320x320"
        return nocache_url
        
    def download_album_image(self):
        url = self.get_album_image()
        response = requests.get(url)
        with open('image.jpg', 'wb') as f:
            f.write(response.content)
        
            

def getDeviceID():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope='user-read-playback-state'))
    playback_info = sp.current_playback()

    if playback_info is None:
        print("\n\n****\n** No device is currently playing. Please start playing music on this device, then rerun. Otherwise, buttons won't work. **\n****\n\n")
        return None

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

#getDeviceID()
