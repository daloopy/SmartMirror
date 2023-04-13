from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock
from home import *
from kivy.uix.label import Label
import subprocess
from kivymd.app import MDApp
from kivymd.uix.button import *
#from motionsensor import *



class MyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)        

    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartupScreen(name="startup"))
        sm.add_widget(Home(name="Home"))
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Gray"
        self.theme_cls.material_style = "M3"
        
        return sm
    
    def on_start(self, time=10):
        # Schedule a function to check for the global variable every second
        #Clock.schedule_interval(self.check_sleep_mode, time)
        pass
        

    def check_sleep_mode(self, *args):
        # Check the value of the global variable
        sleepmode = getSleepMode()
        print("sleep mode value is", sleepmode)
        if (sleepmode):
            subprocess.call("xset dpms force off", shell=True)
            self.on_start(time=1)
        else:
            subprocess.call("xset dpms force on", shell=True)
            self.on_start(time=10)

class StartupScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.welcome = Label(text="Welcome",
                             font_size=48)
        self.add_widget(self.welcome)

    def on_enter(self):
        Clock.schedule_once(self.switch_to_home, 4)

    def switch_to_home(self, *args):
        self.manager.current = "Home"



if __name__ == "__main__":
    MyApp().run()
