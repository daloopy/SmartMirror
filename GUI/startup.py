from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.gridlayout import GridLayout

from kivy.clock import Clock
from kivy.uix.label import Label

from user import *
from settings import *
from keyboard import *
from internet import *

class StartUpApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs) 
    
    def build(self):
        sm = ScreenManager()#transition=FadeTransition())
        sm.add_widget(NameScreen(name="Enter Name"))
        sm.add_widget(NetworkNameScreen(name="Enter Network Name"))
        sm.add_widget(NetworkPasswordScreen(name="Enter Network Password"))
        sm.add_widget(ConnectToWifi(name="Connect"))
        sm.add_widget(ZipScreen(name="Enter Zip"))
        sm.add_widget(ExitScreen(name="Exit"))
        return sm


class NameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols=1)
        self.keyboard = VirtualKeyboard(return_func=self.setName, preset_text="Please enter your name: ")
        self.layout.add_widget(self.keyboard)
        self.add_widget(self.layout)

    def setName(self, input):
        user = User()
        user.set_user_name(input)
        self.manager.current = "Enter Network Name"

class NetworkNameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols=1)
        self.keyboard = VirtualKeyboard(return_func=self.setName, preset_text="Please enter the name of your Wifi Network: ")
        self.layout.add_widget(self.keyboard)
        self.add_widget(self.layout)

    def setName(self, input):
        user = User()
        user.set_user_wifi_name(input)
        self.manager.current = "Enter Network Password"

class NetworkPasswordScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user = User()
        self.layout = GridLayout(cols=1)
        

    def on_enter(self):
        self.wifi_name = self.user.get_user_wifi_name()
        self.keyboard = VirtualKeyboard(return_func=self.setPassword, preset_text="Please enter the password for {}: ".format(self.wifi_name))
        self.layout.add_widget(self.keyboard)
        self.add_widget(self.layout)

    def setPassword(self, input):
        user = User()
        user.set_user_wifi_password(input)
        self.manager.current = "Connect"        

class ConnectToWifi(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols=1)
        self.user = User()
        self.network_name = self.user.get_user_wifi_name()
        self.connect_label = Label(text = "Connecting to network...".format(self.network_name))
        self.layout.add_widget(self.connect_label)
        self.add_widget(self.layout)

    def on_enter(self):
        self.network_name = self.user.get_user_wifi_name()
        self.connect_label.text = "Connecting to {}...".format(self.network_name)
        Clock.schedule_once(self.connect, 5)
    
    def connect(self, *args):
        #connect_to_wifi()
        #wait_for_connection()
        self.connect_label.text = "Connected to {}!".format(self.network_name)
        self.manager.current = "Enter Zip"
    
class ZipScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols=1)
        self.textlabel = Label(text="Please enter your zipcode:")
        self.layout.add_widget(self.textlabel)
        self.keyboard = DigitKeyboard(return_func=self.setZip)
        self.layout.add_widget(self.keyboard)
        self.add_widget(self.layout)

    def setZip(self, input):
        user = User()
        user.set_user_zipcode(input)
        self.manager.current = "Exit"

class ExitScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols=1)
        self.user = User()
        self.username = self.user.get_user_name()
        self.textlabel = Label(text="Thank you, {}!".format(self.username))
        self.layout.add_widget(self.textlabel)
        self.add_widget(self.layout)

    def on_enter(self, *args):
        self.username = self.user.get_user_name()
        self.textlabel.text="Thank you, {}!".format(self.username)
        Clock.schedule_once(self.connected_to, 3)

    def connected_to(self, *args):    
        self.networkname = self.user.get_user_wifi_name()
        self.textlabel.text = "Your current network connection is {}.".format(self.networkname)
        Clock.schedule_once(self.location_is, 3)

    def location_is(self, *args):    
        self.location = self.user.get_user_zipcode()
        self.textlabel.text = "Your current location is {}.".format(self.location)
     

if __name__ == "__main__":
    StartUpApp().run()     