from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from keyboard import *
from functools import partial
from kivy.core.window import WindowBase
from user import *



def settingPopUp(instance):
        # popup = SettingPopUp()
        # popup.open()
        layout = GridLayout(cols = 1, padding = 10)
        popupLabel = Label(text = "Click for pop-up")

        changeZip = Button(text = "Change Zip Code")
        changeZip.bind(on_press=changeZipPopUp)
        changeWiFi = Button(text = "Change WiFi")
        changeWiFi.bind(on_press=changeWiFiPopUp)
        closeButton = Button(text = "Exit Settings")
        changeUser = Button(text = "Change Name")
        changeUser.bind(on_press=changeUserPopUp)
  
        layout.add_widget(popupLabel)
        layout.add_widget(changeZip)
        layout.add_widget(changeWiFi)
        layout.add_widget(changeUser) 
        layout.add_widget(closeButton) 
             
  
        # Instantiate the modal popup and display
        popup = Popup(title ='Settings',
                      content = layout)  
        popup.open()   
  
        # Attach close button press with popup.dismiss action
        closeButton.bind(on_press = popup.dismiss) 
        pass

def changeZipPopUp(instance):
        popup = updateZipPopUp()
        popup.open()
        pass

def changeWiFiPopUp(instance):
        popup = updateWifiPopUp()
        popup.open()
        pass

def changeUserPopUp(instance):
     popup = updateUserPopUp()
     popup.open()
     pass
    
class updateZipPopUp(Popup):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
        self.layout = GridLayout(cols = 1, rows = 3, padding = 10)
        self.title = "Change Zip Code"
        
        
        self.closeButton = Button(text = "Exit")
        self.closeButton.bind(on_press = self.dismiss)
        
        self.keyboard = DigitKeyboard(return_func=self.updateZip)
  
        self.layout.add_widget(self.keyboard, index = 1)
        self.layout.add_widget(self.closeButton, index = 0)   
        
        self.content = self.layout
        self.open()
        pass
        
    def updateZip(self, input):
        user = User()
        user.set_user_zipcode(input)
        #### TO DO: UPDATE WEATHER ON HOME SCREEN (it will update automatically every 5 mins)
        self.dismiss()

    
       
class updateWifiPopUp(Popup):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
        self.layout = GridLayout(cols = 1, rows = 3, padding = 10)
        self.title = "Change wifi"
        
        
        self.closeButton = Button(text = "Exit")
        self.closeButton.bind(on_press = self.dismiss)
        
        self.keyboard = VirtualKeyboard(return_func=self.updateWifi)
  
        self.layout.add_widget(self.keyboard, index = 1)
        self.layout.add_widget(self.closeButton, index = 0)   
        
        self.content = self.layout
        self.open()
        pass
        
    def updateWifi(self, input):
        print("From updateWifi: ", input)
        user = User()
        user.set_user_wifi_name(input)
        self.dismiss()

class updateUserPopUp(Popup):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
        self.layout = GridLayout(cols = 1, rows = 3, padding = 10)
        self.title = "Change Name"
        
        
        self.closeButton = Button(text = "Exit")
        self.closeButton.bind(on_press = self.dismiss)
        
        self.keyboard = VirtualKeyboard(return_func=self.updateWifi)
  
        self.layout.add_widget(self.keyboard, index = 1)
        self.layout.add_widget(self.closeButton, index = 0)   
        
        self.content = self.layout
        self.open()
        pass
        
    def updateWifi(self, input):
        print("From updateUser: ", input)
        user = User()
        user.set_user_name(input)
        self.dismiss()