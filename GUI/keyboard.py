from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.vkeyboard import VKeyboard
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup



class VirtualKeyboard(VKeyboard):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create a VirtualKeyboard widget
        self.virtual_keyboard = VKeyboard(on_key_up = self.key_up)
        self.add_widget(self.virtual_keyboard)
        self.text = Label(text='hi')
        self.add_widget(self.text)
        # Add the VirtualKeyboard widget to the content of the popup
        # Create a label to display the input        
        
    def key_up(self, keyboard, keycode, label=None, *args):

        if isinstance(keycode, tuple):
            keycode = keycode[1]

        if not label:
            return

        thing = label.text 
        print(thing)
        
        if keycode == "spacebar":
            keycode = " "
        elif keycode == "backspace":
            thing = thing[:-1]
            keycode = ""
        elif keycode == "enter" or keycode == "escape":
            keycode = ""
            #self.username = f'{thing}'
            #self.layout.remove_widget(keyboard)
            #submit

        label.text = f'{thing}{keycode}'
        pass
    

class DigitKeyboard(VKeyboard):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def key_up(self):
        pass

class VirtualKeyboardLayout(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = 1
        self.virtual_keyboard = VirtualKeyboard()
        self.add_widget(self.virtual_keyboard)
        

    pass