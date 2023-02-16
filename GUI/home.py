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
import os
from kivy.uix.popup import Popup


#Builder.load_file('smartmirror.kv')


class WeatherTimeDisplay(FloatLayout):    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        town, temp, condition = getWeather()
        self.date_label = Label(text=datetime.now().strftime("%B %d, %Y"),
                                size_hint=(0.5, 0.5),
                                pos_hint={"left": 0, "top":1},
                                font_size= 48)
        self.time_label = Label(text=datetime.now().strftime("%I:%M"),
                                size_hint=(0.5, 0.5),
                                pos_hint={"left": 0, "top":0.90},
                                font_size= 72)  
        self.weather_label = Label(text="{}°F  {}".format(temp, condition),
                                    size_hint=(0.5, 0.5),
                                    pos_hint={"left": 0, "top":0.80},
                                    font_size= 48)
        self.town_label = Label(text="{}".format(town),
                                    size_hint=(0.5, 0.5),
                                    pos_hint={"left": 0, "top":0.70},
                                    font_size= 48)
        
        self.settings_btn = Button(text="settings",
                                size_hint=(0.1, 0.1),
                                pos_hint={"right":1},
                                font_size= 36)

        self.settings_btn.bind(on_press=settingPopUp)

        self.add_widget(self.weather_label)
        self.add_widget(self.time_label)
        self.add_widget(self.date_label)
        self.add_widget(self.town_label)
        self.add_widget(self.settings_btn)

        
        Clock.schedule_interval(self.update_time, 1)
        Clock.schedule_interval(self.update_weather, 300) # update every 5 minutes -> max 288 calls in 1 day

    def update_time(self, dt):
        self.time_label.text = datetime.now().strftime("%I:%M %p")
        self.date_label.text = datetime.now().strftime("%B %d, %Y")

    def update_weather(self, dt):
        town, temp, condition = getWeather()
        self.weather_label.text = "{}°F  {}".format(temp, condition)


class WeatherTimeApp(App):
    def build(self):
        return WeatherTimeDisplay()

if __name__ == "__main__":
    WeatherTimeApp().run()
