from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.vkeyboard import VKeyboard
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup



class VirtualKeyboard(VKeyboard):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create a VirtualKeyboard widget
        self.virtual_keyboard = VKeyboard(on_key_up = self.key_up)
        self.add_widget(self.virtual_keyboard)
        # Add the VirtualKeyboard widget to the content of the popup
        self.content = self.virtual_keyboard


        # Create a label to display the input
        self.label = Label(text='', font_size=30)
        self.add_widget(self.label)
        
        

        

    def key_up(self, keyboard, keycode, *args):
        if isinstance(keycode, tuple):
            keycode = keycode[1]

        thing = self.label.text 
        
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