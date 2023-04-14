from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from keyboard import *
from functools import partial
from kivy.core.window import WindowBase



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
  
        layout.add_widget(popupLabel)
        layout.add_widget(changeZip)
        layout.add_widget(changeWiFi)
        layout.add_widget(closeButton)       
  
        # Instantiate the modal popup and display
        popup = Popup(title ='Settings',
                      content = layout)  
        popup.open()   
  
        # Attach close button press with popup.dismiss action
        closeButton.bind(on_press = popup.dismiss) 
        pass

def changeZipPopUp(instance):
        zipcode = "47906"
        layout = GridLayout(cols = 1, rows = 3, padding = 10)
        #popupLabel = Label(text = "Current Zipcode: {}".format(zipcode))
        closeButton = Button(text = "Exit")
        keyboard = VirtualKeyboard(return_func=updateZip)
  
        #layout.add_widget(popupLabel, index = 2)
        layout.add_widget(keyboard, index = 1)
        layout.add_widget(closeButton, index = 0)  

  
        # Instantiate the modal popup and display
        popup = Popup(title ='Change Zip Code',
                      content = layout)  
        popup.open()   

        # # Attach close button press with popup.dismiss action
        closeButton.bind(on_press = popup.dismiss) 
        pass

def changeWiFiPopUp(instance):
        layout = GridLayout(cols = 1, padding = 10)
        popupLabel = Label(text = "Please enter new WiFi, or click exit")

        closeButton = Button(text = "Exit")
  
        layout.add_widget(popupLabel)
        layout.add_widget(closeButton)       
  
        # Instantiate the modal popup and display
        popup = Popup(title ='Change WiFi',
                      content = layout)  
        popup.open()   
  
        # Attach close button press with popup.dismiss action
        closeButton.bind(on_press = popup.dismiss) 
        pass
    
def updateZip(input):
    print("From updateZip: ", input)
    

class DigitKeyboardPopUp(Popup):
    def __init__(self, **kwargs):
        super(Popup, self).__init__(**kwargs)
        self.vkeyboardlayout = VirtualKeyboardLayout()
        self.content = self.vkeyboardlayout 
        self.vkeyboardlayout.virtual_keyboard.pos_hint = { "top": 0, "right": 1 }

