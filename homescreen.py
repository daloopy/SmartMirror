from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.vkeyboard import VKeyboard
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window

Window.size = (1440,1600) # full screen on Mac 13 inch

class SmartMirror(App):
    def build(self):
        self.layout = GridLayout(cols = 1)
        self.layout.add_widget(WeatherDisplay())
        return self.layout

class WeatherDisplay(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1

        self.weather_label = Label(text="Weather: 75°F, Sunny",
                                    size_hint=(1, 0.1),
                                    pos_hint={"x": 0, "bottom": 1})
        self.add_widget(self.weather_label)



if __name__ == "__main__":
    SmartMirror().run()    
