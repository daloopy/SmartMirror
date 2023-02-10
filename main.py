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
        self.window = GridLayout()
        self.window.cols = 3
        self.window.size_hint = (0.6, 0.7) # tuple (side margin %, top/bottom margin %)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        #add widgets to window
        #self.window.add_widget(welcomeScreen())
        self.window.add_widget(enterName())
        self.window.add_widget(keyboard())

        return self.window

    
class welcomeScreen(Label):
    def __init__(self, **kwargs):
        super(welcomeScreen, self).__init__(**kwargs)
        self.text="Good Morning"
        self.font_size = 78
        
class enterName(Label):
    def __init__(self, **kwargs):
        super(enterName, self).__init__(**kwargs)
        self.text="Please enter your name:"
        self.font_size = 78

class keyboard(VKeyboard):
    
    def __init__(self, **kwargs):
        super(VKeyboard, self).__init__(**kwargs)
        self.on_key_up = self.key_up(self.keycode)


    def key_up(self, keycode, *args):
        if isinstance(keycode, tuple):
            keycode = keycode[1] # second item

        pass

if __name__ == "__main__":
    SmartMirror().run()