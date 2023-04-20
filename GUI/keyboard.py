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


class VirtualKeyboard(GridLayout):
    def __init__(self, return_func=None, preset_text="Enter input: ", **kwargs):
        super().__init__(**kwargs)
        self.return_func = return_func
        self.cols = 1
        self.rows = 2
        self.preset_text = preset_text

        # Create a VirtualKeyboard widget
        self.virtual_keyboard = VKeyboard(on_key_up = self.key_up)
        self.add_widget(self.virtual_keyboard, index = 1)
        self.caps_lock = False
        
        # create label that will be updated
        self.input = Label(text=preset_text)
        self.add_widget(self.input, index = 0)
      
        
    def key_up(self, keyboard, keycode, label=None, *args):
        if isinstance(keycode, tuple):
            keycode = keycode[1]

        thing = self.input.text
        self.shift = False
        
        if (thing == self.preset_text):
            thing = ""

        # keycode translations
        if keycode == "spacebar":
            keycode = " "
        elif keycode == "tab":
            keycode = "  "
        elif keycode == "capslock":
            keycode = ""
            self.caps_lock = not self.caps_lock
        elif keycode == "shift":
            keycode = ""
            self.shift = True
        elif keycode == "layout":
            keycode = ""
        elif keycode == "backspace":
            thing = thing[:-1]
            keycode = ""
        elif keycode == "enter" or keycode == "escape":
            keycode = ""
            if(self.return_func is not None):
                self.return_func(self.input.text)

        if self.caps_lock == True or self.shift == True:
            keycode = keycode.upper()

        # update label
        self.input.text = f'{thing}{keycode}'
        pass
    

class DigitKeyboard(BoxLayout):
    def __init__(self, return_func=None, **kwargs):
        super().__init__(**kwargs)
        self.return_func = return_func
        self.input = Label(text = "")
        self.add_widget(self.input)
        
        for i in range(10):
            digit = Button(text=str(i), size_hint=(0.2,0.2))
            digit.bind(on_release=lambda button: self.appendInput(button.text))
            self.add_widget(digit)
        
        self.enter = Button(text="Enter", size_hint=(0.2,0.2))
        self.enter.bind(on_press = self.exitPopup)
        self.add_widget(self.enter)

        self.delete = Button(text="Delete", size_hint=(0.2,0.2))
        self.delete.bind(on_press = self.deleteInput)
        self.add_widget(self.delete)
        
    def appendInput(self, text):
        if(len(self.input.text) < 5):
            self.input.text = self.input.text + str(text)
        pass

    def deleteInput(self, dt):
        self.input.text = self.input.text[:-1]
        pass
    
    def exitPopup(self, dt):
        if(self.return_func is not None):
                self.return_func(self.input.text)
