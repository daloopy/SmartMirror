from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.vkeyboard import VKeyboard
from kivy.uix.gridlayout import GridLayout


class SmartMirror(App):
    def build(self):
        self.layout = GridLayout(cols = 1)
        self.username = ""
        keyboard = VKeyboard(on_key_up = self.key_up)
        self.label = Label(text = "Please enter your name")
        self.layout.add_widget(self.label)
        self.layout.add_widget(keyboard)
        return self.layout

    def key_up(self, keyboard, keycode, *args):
        if isinstance(keycode, tuple):
            keycode = keycode[1]

        thing = self.label.text 
        if thing == "Please enter your name" :
            thing = ""
        
        if keycode == "spacebar":
            keycode = " "
        elif keycode == "backspace":
            thing = thing[:-1]
            keycode = ""
        elif keycode == "enter" or keycode == "escape":
            keycode = ""
            self.username = f'{thing}'
            self.layout.remove_widget(keyboard)
            #submit

        self.label.text = f'{thing}{keycode}'
        pass

if __name__ == "__main__":
    SmartMirror().run()