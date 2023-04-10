from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock
from home import *
from kivy.uix.label import Label
#from motionsensor import *



class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)        

    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartupScreen(name="startup"))
        sm.add_widget(Home(name="Home"))
        sm.add_widget(SleepScreen(name="Sleep"))
        return sm
    
    def on_start(self):
        # Schedule a function to check for the global variable every second
        Clock.schedule_interval(self.check_sleep_mode, 1)
        

    def check_sleep_mode(self, *args):
        # Check the value of the global variable
        
        sleepmode = False #getSleepMode()
        print("sleep mode value is", sleepmode)
        if sleepmode:
            #sleepmode = False
            # If it's true, switch to the Sleep screen
            self.root.current = "Sleep"
        else:
            #sleepmode = True
            # Otherwise, switch to the Home screen
            self.root.current = "Home"

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
