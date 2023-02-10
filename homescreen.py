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
        self.layout = GridLayout(cols = 3)
        btn = Button(text = "click here")
        self.layout.add_widget(btn)
        return self.layout

    

if __name__ == "__main__":
    SmartMirror().run()