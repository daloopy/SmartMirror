import kivy
kivy.require("1.11.1")
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.lang import Builder
from datetime import datetime
from weatherapi import *
from settings import *
from motionsensor import *
from spotify import *
import os
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.popup import Popup
from kivymd.uix.screen import MDScreen
from kivymd.icon_definitions import md_icons
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.label import MDLabel
from kivymd.font_definitions import theme_font_styles
from kivymd.uix.circularlayout import MDCircularLayout
#from kivymd.uix.girdlayout import MDGridLayout
from kivymd.uix.floatlayout import MDFloatLayout


class Home(MDScreen):    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = MDFloatLayout(pos = self.pos, size = self.size, radius = [25,0,0,0])
        self.index = 0
        town, temp, condition = getWeather()
        self.date_label = MDLabel(text=datetime.now().strftime("%B %d, %Y"),
                                size_hint=(0.5, 0.5),
                                pos_hint={"left": 0, "top":1},
                                font_size= 48, font_style = "H4")
        self.time_label = MDLabel(text=datetime.now().strftime("%I:%M"),
                                size_hint=(0.5, 0.5),
                                pos_hint={"left": 0, "top":0.90},
                                font_size= 72, font_style = "H3")  
        self.weather_label = MDLabel(text="{}°F  {}".format(temp, condition),
                                    size_hint=(0.5, 0.5),
                                    pos_hint={"left": 0, "top":0.80},
                                    font_size= 48, font_style = "H4")
        self.town_label = MDLabel(text="{}".format(town),
                                    size_hint=(0.5, 0.5),
                                    pos_hint={"left": 0, "top":0.70},
                                    font_size= 48, font_style = "H4")
        
        self.settings_btn = MDFloatingActionButton(icon="cog",
                                                theme_icon_color="Custom", size_hint = (0.1, 0.1),
                                                pos_hint={"right":1}, icon_size = "64")

        self.settings_btn.bind(on_press=settingPopUp)

        self.togglewidgets = MDFloatingActionButton(icon="refresh",
                                                theme_icon_color="Custom", size_hint = (0.1, 0.1),
                                                pos_hint={"right":1, "top": 1}, icon_size = "64")
        self.togglewidgets.bind(on_press=self.cycle_widgets)

        # define widgets here ****************************
        self.spotify_player = SpotifyPlayer()
        #self.calendar = Calendar() # uncomment when created
        #self.sports_widget = Sports() # uncomment when created


        self.layout.add_widget(self.weather_label)
        self.layout.add_widget(self.time_label)
        self.layout.add_widget(self.date_label)
        self.layout.add_widget(self.town_label)
        self.layout.add_widget(self.settings_btn)
        self.layout.add_widget(self.togglewidgets)
        

        self.add_widget(self.layout) # add the GridLayout to the screen
        
        Clock.schedule_interval(self.update_time, 30)
        Clock.schedule_interval(self.update_weather, 120) # update every 5 minutes -> max 288 calls in 1 day

    def update_time(self, dt):
        self.time_label.text = datetime.now().strftime("%I:%M %p")
        self.date_label.text = datetime.now().strftime("%B %d, %Y")

    def update_weather(self, dt):
        town, temp, condition = getWeather()
        self.weather_label.text = "{}°F  {}".format(temp, condition)
        self.town_label.text = "{}".format(town)

    def cycle_widgets(self, dt):
        self.index = (self.index + 1) % 4 # cycle through 3 widgets we will add
        
        if(self.index == 1):
                #pass
                self.layout.add_widget(self.spotify_player)
        elif(self.index == 2):
                #pass
            self.layout.remove_widget(self.spotify_player) # remove previous widgets
            #self.layout.add_widget(self.sports_widget)
        elif(self.index == 3):
            #self.layout.remove_widget(self.sports_widget) # remove previous widgets
            #self.layout.add_widget(self.calendar)
            pass
        elif(self.index == 0):
            # have no widgets on screen
            #self.layout.remove_widget(self.calendar) # remove previous widgets
            pass
