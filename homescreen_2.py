import kivy
kivy.require("1.11.1")
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.lang import Builder
from datetime import datetime
import os

Builder.load_file('smartmirror.kv')
WEATHERAPI_TOKEN=os.getenv("WEATHERAPI_TOKEN")


class WeatherTimeDisplay(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        self.date_label = Label(text=datetime.now().strftime("%B %d, %Y"),
                                size_hint=(0.5, 0.5),
                                pos_hint={"x": 0, "top":1},
                                font_size= 48)
        self.time_label = Label(text=datetime.now().strftime("%H:%M"),
                                size_hint=(0.5, 0.5),
                                pos_hint={"x": 0, "top":0.90},
                                font_size= 72)            
        self.weather_label = Label(text="Weather: 32°F, Cloudy",
                                    size_hint=(0.5, 0.5),
                                    pos_hint={"x": 0, "top":0.80},
                                    font_size= 48)
        
        

        self.add_widget(self.weather_label)
        self.add_widget(self.time_label)
        self.add_widget(self.date_label)
        
        Clock.schedule_interval(self.update_time, 1)

    def update_time(self, dt):
        self.time_label.text = datetime.now().strftime("%H:%M")
        self.date_label.text = datetime.now().strftime("%B %d, %Y")




class WeatherTimeApp(App):
    def build(self):
        return WeatherTimeDisplay()


if __name__ == "__main__":
    WeatherTimeApp().run()
