import kivy
kivy.require("1.11.1")

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.lang import Builder

from datetime import datetime

Builder.load_file('smartmirror.kv')

class WeatherTimeDisplay(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        self.rows = 1

        self.weather_label = Label(text="Weather: 75°F, Sunny",
                                    size_hint=(0.5, 0.5),
                                    pos_hint={"x": 0, "top": 1},
                                    font_size= 48)
        self.time_label = Label(text=datetime.now().strftime("%H:%M:%S"),
                                size_hint=(0.5, 0.5),
                                pos_hint={"right": 1, "top": 1},
                                font_size= 48)

        self.add_widget(self.weather_label)
        self.add_widget(self.time_label)
        
        Clock.schedule_interval(self.update_time, 1)

    def update_time(self, dt):
        self.time_label.text = datetime.now().strftime("%H:%M:%S")

class WeatherTimeApp(App):
    def build(self):
        return WeatherTimeDisplay()

if __name__ == "__main__":
    WeatherTimeApp().run()
