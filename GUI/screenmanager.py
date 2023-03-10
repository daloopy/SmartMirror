from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock
from home import *
from kivy.uix.label import Label


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartupScreen(name="startup"))
        sm.add_widget(Home(name="Home"))
        return sm

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